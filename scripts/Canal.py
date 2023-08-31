import numpy as np
from scipy.io import wavfile

class Canal:
    def __init__(self, walkie1, walkie2 , ruido=0.0):
        potencia_fuente = walkie1.get_potencia()
        potencia_receptor = walkie2.get_potencia()
        distancia_fuente = walkie1.get_distancia_referencia()
        distancia_receptor = walkie2.get_distancia_referencia()

        self.atenuacion = (potencia_fuente / potencia_receptor) * (distancia_receptor / distancia_fuente)
        self.ruido = ruido

    def agregar_ruido(self, rate, señal_modulada):
        # Tomar el valor de atenuación y agregar ruido
        señal_transmitida = señal_modulada * self.atenuacion + np.random.normal(0, self.ruido, len(señal_modulada))

        audio_nombre = 'scripts/audios/audio_modulado_ruido.wav'
        wavfile.write( audio_nombre, rate, señal_transmitida.astype(np.int16))
        print(f"Archivo {audio_nombre} guardado")

    def get_atenuacion(self):
        return self.atenuacion

    def get_ruido(self):
        return self.ruido