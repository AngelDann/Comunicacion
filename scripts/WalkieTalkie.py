import numpy as np
from scipy.io import wavfile
import os
from anytree import AnyNode, RenderTree, PreOrderIter
from collections import Counter
#import headp

class WalkieTalkie:
    def __init__(self, potencia=0.5, distancia_referencia=5000):
        self.bits = 16
        self.potencia = potencia
        self.distancia_referencia = distancia_referencia
        self.frequencia_portadora = 3e+7 #Frecuencia AM
        self.huffman_codes = {}


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
    
    def generarArbol(self, diccionario):
        diccionario_sort = dict(sorted(diccionario.items(), key=lambda item: item[1]))
        
        #for elemento, frecuencia in diccionario_sort.items():
            #print(f"Elemento: {elemento}, Frecuencia: {(frecuencia/longitud) *100}")
        
        cola = []

        for elemento, frecuencia in diccionario_sort.items():
            nodo = AnyNode(id=elemento,
                           frecuencia=frecuencia,
                            izquierda=None,
                            derecha=None,
                            bits= None,
                            )
            cola.append(nodo)
        
        i = 0
        while len(cola) > 1:
            
            nodo_izquierda = cola.pop(0)
            nodo_derecha = cola.pop(0)

            nuevo_nodo = AnyNode(
                id = f"{str(nodo_izquierda.frecuencia) + str(nodo_derecha.frecuencia)}",
                frecuencia=nodo_izquierda.frecuencia + nodo_derecha.frecuencia, 
                izquierda = nodo_izquierda, 
                derecha = nodo_derecha,
                bits = None
            )
            
            #nuevo_nodo.izquierda = nodo_izquierda
            #nuevo_nodo.derecha = nodo_derecha

            cola.append(nuevo_nodo)
            i+=1
        
        arbol_huffman = cola[0]

        return arbol_huffman
    
    def get_huffman_codes(self, node, bits=""):
        if node.izquierda is not None:
            self.get_huffman_codes(node.izquierda, bits + '0')
        if node.derecha is not None:
            self.get_huffman_codes(node.derecha, bits + '1')
        if len(str(node.frecuencia)) == 1:
            self.huffman_codes[node.frecuencia] = bits



    def BotonTransmitir(self, rate, audio_data):
        # Proceso de conversión ADC
        audio_data_normalized = audio_data / np.max(np.abs(audio_data))
        audio_data_quantized = np.round(audio_data_normalized * (2**(self.bits - 1))).astype(np.int16)
        
        #print(RenderTree(arbol_huffman))
        ##########################################################
        # Supongamos que tienes una matriz NumPy
        mi_matriz = np.array([[1, 2, 3],
                            [1, 2, 3],
                            [4, 5, 6],
                            [1, 2, 3],
                            [7, 8, 9]])

        # Usando np.unique con axis para encontrar sublistas únicas
        sublistas_unicas, indices, conteos = np.unique(mi_matriz, axis=0, return_index=True, return_counts=True)

        # Crear un diccionario con las sublistas únicas y sus frecuencias
        diccionario_sublistas = {}

        for sublista, conteo in zip(sublistas_unicas, conteos):
            diccionario_sublistas[tuple(sublista)] = conteo

        # Imprimir el diccionario
        print(diccionario_sublistas)

        arbol = self.generarArbol(diccionario_sublistas)
        print(RenderTree(arbol))

        # Inicializa el diccionario de códigos de Huffman
        self.huffman_codes = {}
        
        # Llama a get_huffman_codes con la raíz del árbol y una cadena vacía para los bits iniciales
        self.get_huffman_codes(arbol, bits="")
        
        # Imprime el diccionario de códigos de Huffman
        print(self.huffman_codes)

        #for char, code in self.huffman_codes.items():
         #   print(f"Caracter: {char}, Codigo Huffman: {code}")

        #data_coded = self.codificar_huffman(mi_matriz)
        #print(data_coded)
        ############################################################


        tiempo = np.arange(len(audio_data)) / rate
        portadora = np.cos(2 * np.pi * self.frequencia_portadora * tiempo)

        # Modulación
        señal_modulada = audio_data_quantized * portadora
        print(señal_modulada)

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