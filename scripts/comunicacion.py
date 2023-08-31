
from WalkieTalkie import WalkieTalkie
from Canal import Canal
import random

#Creacion de 2 walkie talkies para cada persona
#El primer valor es la potencia y el segundo la distancia respecto al punto de referencia del walkie talkie
#Se hace aleatoriamente la distancia desde el punto de referencia para que en el canal se pueda agregar el ruido
walkie1 = WalkieTalkie(1, random.randint(500,2500))
walkie2 = WalkieTalkie(1, random.randint(500,2500))

#Frecuencia AM
print("Frecuencia de Walkie-Talkies: Walkie1=", walkie1.get_frecuencia_portadora(), "Walkie2=",walkie2.get_frecuencia_portadora())

#Fuente de Informacion
rate,audio_data = walkie1.FuenteInformacion("scripts/guitar.wav")

# Transmisión
rate,señal_modulada = walkie1.BotonTransmitir(rate,audio_data)

#Canal
canal = Canal(walkie1, walkie2, random.randint(0,10))
print("Atenuacion:", canal.get_atenuacion(), "Ruido:", canal.get_ruido())
canal.agregar_ruido(rate, señal_modulada)

# Recepción
walkie2.BotonRecibir('scripts/audios/audio_modulado_ruido.wav')

#Destino Final
walkie2.reproducir('scripts/audios/audio_recibido.wav')