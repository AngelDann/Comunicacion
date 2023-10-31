import numpy as np
from scipy.io import wavfile
import random as r
import math

class Canal:
    def __init__(self, walkie1, walkie2):
        self.codificacion1 = walkie1.get_codificacion()
        self.codificacion2 = walkie2.get_codificacion()
        potencia_fuente = walkie1.get_potencia()
        potencia_receptor = walkie2.get_potencia()
        distancia_fuente = walkie1.get_distancia_referencia()
        distancia_receptor = walkie2.get_distancia_referencia()

        self.atenuacion = (potencia_fuente / potencia_receptor) * (distancia_receptor / distancia_fuente)

        self.señal_transmitida = []
        self.num_aleatorios = []
        self.canales = [[] for _ in range(5)] #Canales en total
        self.probabilidades_ruido = [0.7, 0.2, 0.1, 0.4, 0.8] #La probabilidad de ruido que tiene cada canal

    def pasoInformacion(self, rate, señal_modulada, codificado):
        if self.codificacion1 == 0 and self.codificacion2 == 0:
            self.procesarSeñalModulada(rate, señal_modulada)
        else:
            self.procesarCodificado(codificado)

    def procesarSeñalModulada(self, rate, señal_modulada):
        duracion_segmento = 0.001
        duracion_total = len(señal_modulada) / float(rate)
        num_segmentos = int(np.ceil(duracion_total / duracion_segmento))

        for i in range(num_segmentos):
            inicio = int(i * rate * duracion_segmento)
            fin = int((i + 1) * rate * duracion_segmento)
            segmento = señal_modulada[inicio:fin]
            self.agregar_ruido(segmento)

        self.calcular_entropia()
        self.guardar_audio(rate)

    def procesarCodificado(self, codificado):
        print(len(codificado))
        i = 0
        j = 0
        while i < len(codificado):
            elem = codificado[i]
            if self.agregarRuidoEnCodificado(probabilidad=self.probabilidades_ruido[j]):
                codificado = np.delete(codificado, i)
                if j < len(self.canales)-1:
                    j+=1 #Cambio de canal a otro que no tenga ruido
                else:
                    j = 0
            else:
                self.canales[j].append(elem) #Sigue en el mismo canal
                i += 1
        print(len(codificado))
        for elem in self.canales:
            print(len(elem))

    def agregarRuidoEnCodificado(self, probabilidad):
        # Si la probabilidad es menor que 0.06 (6%), se elimina el elemento
        if r.random() < probabilidad:
            return True
        return False

    def agregar_ruido(self, segmento):
        aleatorio = r.randint(0,100)
        if aleatorio in range(20,26):
            self.num_aleatorios.append(0)
            segmento_ruido = segmento * 10
            self.señal_transmitida.extend(segmento_ruido)
        else:
            self.señal_transmitida.extend(segmento)
            self.num_aleatorios.append(1)

    def calcular_entropia(self):
        num_aleatorios = np.array(self.num_aleatorios)
        conteos = np.unique(num_aleatorios, return_counts=True)
        longitud = len(num_aleatorios)
        shannon_entropy = 0

        for i in range(len(conteos[0])):
            n = conteos[1][i]
            p = n/longitud
            shannon_entropy += -p*(math.log(p, 2))
            print(shannon_entropy)

        print("Entropia final:",shannon_entropy)

    def guardar_audio(self, rate):
        #La señal con ruido se vuelve a convertir en array para la transformacion en audio       
        print("Max:",max(self.num_aleatorios), "Min:", min(self.num_aleatorios), "Longitud:", len(self.num_aleatorios))
        señal_transmitida = np.array(self.señal_transmitida)

        # Tomar el valor de atenuación y agregar ruido

        audio_nombre = 'scripts/audios/audio_modulado_ruido.wav'
        wavfile.write(audio_nombre, rate, señal_transmitida.astype(np.int16))
        print(f"Archivo {audio_nombre} guardado")


    def get_atenuacion(self):
        return self.atenuacion