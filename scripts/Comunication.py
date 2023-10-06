import numpy as np
from scipy.io import wavfile
import random as r
import math

class Canal:
    def __init__(self, walkie1, walkie2):
        potencia_fuente = walkie1.get_potencia()
        potencia_receptor = walkie2.get_potencia()
        distancia_fuente = walkie1.get_distancia_referencia()
        distancia_receptor = walkie2.get_distancia_referencia()

        self.atenuacion = (potencia_fuente / potencia_receptor) * (distancia_receptor / distancia_fuente)

    def agregar_ruido(self, rate, señal_modulada):
        duracion_segmento = 0.001
        duracion_total = len(señal_modulada) / float(rate)
        num_segmentos = int(np.ceil(duracion_total / duracion_segmento))
        señal_transmitida = []
        num_aleatorios = []

        for i in range(num_segmentos):
            aleatorio = r.randint(0,100)
            inicio = int(i * rate * duracion_segmento)
            fin = int((i + 1) * rate * duracion_segmento)
            segmento = señal_modulada[inicio:fin]

            if aleatorio in range(20,26):
                num_aleatorios.append(0)
                segmento_ruido = segmento * 10
                señal_transmitida.extend(segmento_ruido)
            else:
                señal_transmitida.extend(segmento)
                num_aleatorios.append(1)
        
        num_aleatorios = np.array(num_aleatorios)
        conteos = np.unique(num_aleatorios, return_counts=True)
        longitud = len(num_aleatorios)
        shannon_entropy = 0

        for i in range(len(conteos[0])):
            n = conteos[1][i]
            p = n/longitud
            shannon_entropy += -p*(math.log(p, 2))
            print(shannon_entropy)

        print("Entropia final:",shannon_entropy)

        #La señal con ruido se vuelve a convertir en array para la transformacion en audio       
        print("Max:",max(num_aleatorios), "Min:", min(num_aleatorios), "Longitud:", len(num_aleatorios))
        señal_transmitida = np.array(señal_transmitida)

        # Tomar el valor de atenuación y agregar ruido

        audio_nombre = 'scripts/audios/audio_modulado_ruido.wav'
        wavfile.write( audio_nombre, rate, señal_transmitida.astype(np.int16))
        print(f"Archivo {audio_nombre} guardado")

    def get_atenuacion(self):
        return self.atenuacion

import numpy as np
from scipy.io import wavfile
import os

class WalkieTalkie:
    def __init__(self, potencia=0.5, distancia_referencia=5000):
        self.bits = 16
        self.potencia = potencia
        self.distancia_referencia = distancia_referencia
        self.frequencia_portadora = 3e+7 #Frecuencia AM


    #Recibe un archivo stereo que transforma a mono para transmitir la informacion usando la frecuencia portadora
    def FuenteInformacion(self, archivo_audio):
        rate, data_stereo = wavfile.read(archivo_audio)
        data_mono = (data_stereo[:, 0] + data_stereo[:, 1]) / 2
        return rate, data_mono

    def BotonTransmitir(self, rate, audio_data):
        # Proceso de conversión ADC
        audio_data_normalized = audio_data / np.max(np.abs(audio_data))
        audio_data_quantized = np.round(audio_data_normalized * (2**(self.bits - 1))).astype(np.int16)


        tiempo = np.arange(len(audio_data)) / rate
        portadora = np.cos(2 * np.pi * self.frequencia_portadora * tiempo)

        # Modulación
        señal_modulada = audio_data_quantized * portadora

        audio_nombre = 'scripts/audios/audio_modulado.wav'
        wavfile.write( audio_nombre, rate, señal_modulada.astype(np.int16))
        print(f"Archivo {audio_nombre} guardado")
        
        return rate,señal_modulada

    def BotonRecibir(self, audio_nombre):
        rate_received, señal_modulada_mono = wavfile.read(audio_nombre)

        tiempo = np.arange(len(señal_modulada_mono)) / rate_received
        portadora = np.cos(2 * np.pi * self.frequencia_portadora * tiempo)

        # Demodulación
        señal_demodulada = señal_modulada_mono / portadora

        # Conversión a valores originales
        audio_data_original = np.round(señal_demodulada).astype(np.int16)

        # Creación de señal estéreo
        audio_data_original_stereo = np.column_stack((audio_data_original, audio_data_original))

        audio_nombre_original = 'scripts/audios/audio_recibido.wav'
        wavfile.write(audio_nombre_original, rate_received, audio_data_original_stereo)
        print(f"Archivo {audio_nombre_original} guardado")


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

    def get_frecuencia_portadora(self):
        return self.frequencia_portadora

    def get_potencia(self):
        return self.potencia
    
    def get_distancia_referencia(self):
        return self.distancia_referencia


from WalkieTalkie import WalkieTalkie
from Canal import Canal
import random

#Creacion de 2 walkie talkies para cada persona
#El primer valor es la potencia y el segundo la distancia respecto al punto de referencia del walkie talkie
#Se hace aleatoriamente la distancia desde el punto de referencia para que en el canal se pueda agregar el ruido
walkie1 = WalkieTalkie(1, random.randint(500,2500))
walkie2 = WalkieTalkie(1, random.randint(500,2500))

#Frecuencia AM
print("Frecuencia de Walkie-Talkies: Walkie1=", walkie1.get_frecuencia_portadora(), "Walkie2=",walkie2.get_frecuencia_portadora())

#Fuente de Informacion
rate,audio_data = walkie1.FuenteInformacion("scripts/guitar.wav")

# Transmisión
rate,señal_modulada = walkie1.BotonTransmitir(rate,audio_data)

#Canal
canal = Canal(walkie1, walkie2)
print("Atenuacion:", canal.get_atenuacion())
canal.agregar_ruido(rate, señal_modulada)

# Recepción
walkie2.BotonRecibir('scripts/audios/audio_modulado_ruido.wav')

#Destino Final
walkie2.reproducir('scripts/audios/audio_recibido.wav')