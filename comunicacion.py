
from WalkieTalkie import WalkieTalkie


canal = 3
audio = "guitar.wav"

radio = WalkieTalkie(canal)
rate,audio = radio.fuenteInformacion(audio)
radio.transmitir(rate,audio)