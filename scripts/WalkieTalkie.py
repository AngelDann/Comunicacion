import numpy as np
from scipy.io import wavfile
import os
from anytree import AnyNode, RenderTree, PreOrderIter
from collections import Counter
from Codificacion import Codificacion
#import headp

class WalkieTalkie:
    def __init__(self, potencia=0.5, distancia_referencia=5000, tipo_codificacion=0):
        self.bits = 16
        self.potencia = potencia
        self.distancia_referencia = distancia_referencia
        self.frequencia_portadora = 3e+7 #Frecuencia AM
        self.tipo_codificacion = tipo_codificacion
        self.codificacion = Codificacion()


    #Recibe un archivo stereo que transforma a mono para transmitir la informacion usando la frecuencia portadora
    def FuenteInformacion(self, archivo_audio):
        rate, data_stereo = wavfile.read(archivo_audio)
        data_mono = (data_stereo[:, 0] + data_stereo[:, 1]) / 2
        return rate, data_mono

        
    def calcular_divisores(self, numero):
        divisores = []

        for i in range(1, numero + 1):
            if numero % i == 0:
                divisores.append(i)
        return divisores[round(len(divisores)/2)]

    def crearDiccionario(self, informacion):
        # Usando np.unique con axis para encontrar sublistas únicas
        sublistas_unicas, indices, conteos = np.unique(informacion, axis=0, return_index=True, return_counts=True)

        # Crear un diccionario con las sublistas únicas y sus frecuencias
        diccionario_sublistas = {}

        for sublista, conteo in zip(sublistas_unicas, conteos):
            diccionario_sublistas[tuple(sublista)] = conteo
        
        return diccionario_sublistas
    
    def codificacionInformacion(self, informacion):
        longitud = len(informacion)
        divisores = self.calcular_divisores(longitud)
        print("La frecuencia mediana es:", divisores)

        informacion_split = np.array_split(informacion, divisores)
        #Creo el diccionario para la codificacion
        diccionario = self.crearDiccionario(informacion_split)

        #Genero el arbol
        if self.tipo_codificacion == 1:
            arbol = self.codificacion.generarArbolHuffman(diccionario)
            #Creo el handshake
            self.codificacion.generarCodigos(arbol, bits="")
            handshake = self.codificacion.get_codes()
            return self.codificacion.encoding(informacion_split, handshake), handshake
        
        elif self.tipo_codificacion == 2:
            arbol = self.codificacion.generarArbolShannon(diccionario)
            #Creo el handshake
            self.codificacion.generarCodigos(arbol, bits="")
            handshake = self.codificacion.get_codes()
            return self.codificacion.encoding(informacion_split, handshake), handshake
        
        elif self.tipo_codificacion == 3:
            informacion_b64 = self.codificacion.encriptarB64(informacion_split)
            handshake = self.codificacion.handshakeB64(diccionario)
            return informacion_b64, handshake
        
        elif self.tipo_codificacion == 4:
            informacion_RLL = self.codificacion.encriptarRLL(informacion_split)
            return informacion_RLL, None


    def BotonTransmitir(self, rate, audio_data):
        # Proceso de conversión ADC
        audio_data_normalized = audio_data / np.max(np.abs(audio_data))
        audio_data_quantized = np.round(audio_data_normalized * (2**(self.bits - 1))).astype(np.int16)

        tiempo = np.arange(len(audio_data)) / rate
        portadora = np.cos(2 * np.pi * self.frequencia_portadora * tiempo)

        # Modulación
        señal_modulada = audio_data_quantized * portadora
        self.guardar_audio('./scripts/audios/audio_modulado.wav', rate, señal_modulada)

        if self.tipo_codificacion == 0:
            codificado = None
            handshake = None
            return rate,señal_modulada, codificado, handshake
        else:
            codificado, handshake = self.codificacionInformacion(señal_modulada)
            return rate,señal_modulada, codificado, handshake

    def BotonRecibir(self, audio_nombre, codificado=None, handshake=None, lista_canales=None):
        rate_received, señal_modulada_mono = wavfile.read(audio_nombre)

        tiempo = np.arange(len(señal_modulada_mono)) / rate_received
        portadora = np.cos(2 * np.pi * self.frequencia_portadora * tiempo)

        #Decodificacion
        if self.tipo_codificacion == 0:
            señal_demodulada = señal_modulada_mono / portadora
        elif self.tipo_codificacion == 1:
            # Demodulación
            lista_plana = [tupla for sublista in lista_canales for tupla in sublista]
            lista_plana.sort(key=lambda tupla: tupla[0])
            lista_final = [tupla[1] for tupla in lista_plana]
            #print(handshake)
            señal_modulada_mono_decodificada = self.codificacion.decoding(handshake, lista_final)#Como esta dividido se tiene que volver a hacer unidimensional
            señal_demodulada = señal_modulada_mono_decodificada.flatten() / portadora
        elif self.tipo_codificacion == 2:
            lista_plana = [tupla for sublista in lista_canales for tupla in sublista]
            lista_plana.sort(key=lambda tupla: tupla[0])
            lista_final = [tupla[1] for tupla in lista_plana]
             # Demodulación
            señal_modulada_mono_decodificada = self.codificacion.decoding(handshake, codificado)
            #Como esta dividido se tiene que volver a hacer unidimensional
            señal_demodulada = señal_modulada_mono_decodificada.flatten() / portadora
        elif self.tipo_codificacion == 3:
            lista_plana = [tupla for sublista in lista_canales for tupla in sublista]
            lista_plana.sort(key=lambda tupla: tupla[0])
            lista_final = [tupla[1] for tupla in lista_plana]
            señal_modulada_mono_decodificada = self.codificacion.decodingB64(handshake, codificado)
            señal_demodulada = señal_modulada_mono_decodificada.flatten() / portadora
        elif self.tipo_codificacion == 4:
            lista_plana = [tupla for sublista in lista_canales for tupla in sublista]
            lista_plana.sort(key=lambda tupla: tupla[0])
            lista_final = [tupla[1] for tupla in lista_plana]
            señal_modulada_mono_decodificada = self.codificacion.decodificarRLL(codificado)
            señal_demodulada = señal_modulada_mono_decodificada.flatten() / portadora

        # Conversión a valores originales
        audio_data_original = np.round(señal_demodulada).astype(np.int16)

        # Creación de señal estéreo
        audio_data_original_stereo = np.column_stack((audio_data_original, audio_data_original))

        #Se guarda el archivo de audio
        self.guardar_audio('./scripts/audios/audio_recibido.wav', rate_received, audio_data_original_stereo)


    def reproducir(self,audio_filename):
        try:
            # Verificar si el sistema operativo es Windows
            if os.name == 'nt':
                os.system(f'start {audio_filename}')
            # Verificar si el sistema operativo es macOS o Linux
            elif os.name == 'posix':
                os.system(f'open {audio_filename}')
            else:
                print("No se pudo determinar el sistema operativo compatible.")
        except Exception as e:
            print(f"Error al reproducir el audio: {e}")

    def guardar_audio(self, audio_nombre, rate, señal_modulada):
        wavfile.write(audio_nombre, rate, señal_modulada.astype(np.int16))
        print(f"Archivo {audio_nombre} guardado")

    def get_codificacion(self):
        return self.codificacion

    def get_frecuencia_portadora(self):
        return self.frequencia_portadora

    def get_potencia(self):
        return self.potencia
    
    def get_distancia_referencia(self):
        return self.distancia_referencia