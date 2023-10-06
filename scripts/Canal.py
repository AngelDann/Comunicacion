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