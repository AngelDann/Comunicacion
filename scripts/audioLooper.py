import numpy as np
from scipy.io import wavfile

# Cargar el archivo de audio original
archivo_audio_original = 'scripts/guitar.wav'
rate, data = wavfile.read(archivo_audio_original)

# Repetir el audio original tres veces para obtener un audio de 30 segundos
n_repeticiones = 3
audio_extendido = np.tile(data, (n_repeticiones, 1))

# Guardar el audio extendido en un nuevo archivo WAV
archivo_audio_extendido = 'scripts/audio_extendido.wav'
wavfile.write(archivo_audio_extendido, rate, audio_extendido.astype(np.int16))

print(f"Audio repetido {n_repeticiones} veces y guardado en '{archivo_audio_extendido}' (30 segundos de duración).")
