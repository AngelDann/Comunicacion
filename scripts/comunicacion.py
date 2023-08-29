
from WalkieTalkie import WalkieTalkie

# Uso de la clase WalkieTalkie
walkie = WalkieTalkie()

rate,audio_data = walkie.FuenteInformacion("scripts/guitar.wav")

# Transmisión
walkie.BotonTransmitir(rate,audio_data)

# Recepción
walkie.BotonRecibir('audio_modulado.wav')