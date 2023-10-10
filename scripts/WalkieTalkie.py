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
    
    def generarArbol(self, diccionario, longitud):
        diccionario_sort = dict(sorted(diccionario.items(), key=lambda item: item[1]))
        
        #for elemento, frecuencia in diccionario_sort.items():
            #print(f"Elemento: {elemento}, Frecuencia: {(frecuencia/longitud) *100}")
        
        cola = []

        for elemento, frecuencia in diccionario_sort.items():
            nodo = AnyNode(id=elemento,
                            izquierda=None,
                            derecha=None,
                            frecuencia=frecuencia, 
                            )
            cola.append(nodo)
        
        i = 0
        while len(cola) > 1:
            
            nodo_izquierda = cola.pop(0)
            nodo_derecha = cola.pop(0)

            nuevo_nodo = AnyNode(
                id = f"{i}",
                frecuencia=nodo_izquierda.frecuencia + nodo_derecha.frecuencia, 
                izquierda = nodo_izquierda, 
                derecha = nodo_derecha 
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
        if len(str(node.id)) == 1:
            self.huffman_codes[node.id] = bits
        

    def BotonTransmitir(self, rate, audio_data):
        # Proceso de conversión ADC
        audio_data_normalized = audio_data / np.max(np.abs(audio_data))
        audio_data_quantized = np.round(audio_data_normalized * (2**(self.bits - 1))).astype(np.int16)

        #print("la mediana es",self.calcular_divisores(len(audio_data_quantized)), "la longitud es", len(audio_data_quantized))
        longitud = len(audio_data_quantized)
        frecuencia_maxima = self.calcular_divisores(longitud)
        print("La frecuencia máxima es:", frecuencia_maxima)

        audio_data_quantized_split = np.array_split(audio_data_quantized, frecuencia_maxima)

        #for elem in audio_data_quantized_split:
            #print(elem)
    
        valores_unicos, frecuencias = np.unique(audio_data_quantized_split, return_counts=True)
        frecuencia_elementos = dict(zip(valores_unicos, frecuencias))
        
        #print(f"El valor que más se repite es {max_dic_porcentaje} con una frecuencia de {frecuencia_elementos[max_dic_porcentaje]} veces.")

        #for elemento, frecuencia in frecuencia_elementos.items():
            #print(f"Elemento: {elemento}, Frecuencia: {(frecuencia/len(audio_data_quantized_split))* 100}")

        arbol_huffman = self.generarArbol(frecuencia_elementos, longitud)

        nodos_contados = sum(1 for _ in RenderTree(arbol_huffman))

        # Imprimir la cantidad de nodos
        print(f"La cantidad de nodos en el árbol de Huffman es: {nodos_contados}")
        print(RenderTree(arbol_huffman))

        self.get_huffman_codes(arbol_huffman)
        for char, code in self.huffman_codes.items():
            print(f"Caracter: {char}, Codigo Huffman: {code}")

        
        #print(RenderTree(arbol_huffman))

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