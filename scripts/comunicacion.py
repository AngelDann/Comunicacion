
from WalkieTalkie import WalkieTalkie

walkie = WalkieTalkie(1)

rate,audio_data = walkie.FuenteInformacion("scripts/guitar.wav")

# Transmisión
walkie.BotonTransmitir(rate,audio_data)

# Recepción
walkie.BotonRecibir('scripts/audios/audio_modulado.wav')

walkie.reproducir('scripts/audios/audio_recibido.wav')