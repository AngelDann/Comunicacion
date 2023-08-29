import scipy.io.wavfile as wavfile
import numpy as np

class WalkieTalkie:
    
    def __init__(self, channel):
        self.canal = channel
        self.alcance = 10


    def fuenteInformacion(self,archivo_audio):
        rate, audio_data = wavfile.read(archivo_audio)
        return rate, audio_data

    def transmitir(self,rate, audio_data):

        # Proceso de conversión ADC
        bits = 16

        #El audio se transforma en mono
        audio_data = audio_data.mean(axis=1)

        audio_data_normalized = audio_data / np.max(np.abs(audio_data))
        audio_data_quantized = np.round(audio_data_normalized * (2**(bits - 1))).astype(np.int16)

        frecuencia_portadora = 3e+7

        # Generar la señal portadora
        tiempo = np.arange(len(audio_data)) / rate
        portadora = np.cos(2 * np.pi * frecuencia_portadora * tiempo)

        # Producto para generar el AM
        señal_modulada = audio_data_quantized * portadora

        wavfile.write('audio_modulado.wav', rate, señal_modulada.astype(np.int16))

