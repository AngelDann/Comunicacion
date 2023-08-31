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