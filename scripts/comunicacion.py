
from WalkieTalkie import WalkieTalkie
from Canal import Canal
import random

def pedir_opcion():
    opciones = ['Sin codificar', 'Huffman', 'Shannon']
    while True:
        print("Por favor, elige una opción:")
        for i, opcion in enumerate(opciones, 0):
            print(f"{i}. {opcion}")
        eleccion = input("Ingresa el número de tu opción: ")
        if eleccion in ['0', '1', '2']:
            return int(eleccion)
        else:
            print("Entrada inválida. Por favor, ingresa un número del 1 al 3.")

def main(opcion=0):

    #Creacion de 2 walkie talkies para cada persona
    #El primer valor es la potencia y el segundo la distancia respecto al punto de referencia del walkie talkie
    #Se hace aleatoriamente la distancia desde el punto de referencia para que en el canal se pueda agregar el ruido
    walkie1 = WalkieTalkie(1, random.randint(500,2500), tipo_codificacion=opcion)
    walkie2 = WalkieTalkie(1, random.randint(500,2500), tipo_codificacion=opcion)

    #Frecuencia AM
    print("Frecuencia de Walkie-Talkies: Walkie1=", walkie1.get_frecuencia_portadora(), "Walkie2=",walkie2.get_frecuencia_portadora())

    #Fuente de Informacion
    rate,audio_data = walkie1.FuenteInformacion("./scripts/alarm.wav")

    # Transmisión
    rate,señal_modulada, codificado, handshake = walkie1.BotonTransmitir(rate,audio_data)

    #Canal
    canal = Canal(walkie1, walkie2)
    print("Atenuacion:", canal.get_atenuacion())
    canal.pasoInformacion(rate, señal_modulada)

    # Recepción
    walkie2.BotonRecibir('./scripts/audios/audio_modulado_ruido.wav', codificado, handshake)

    #Destino Final
    #walkie2.reproducir('scripts/audios/audio_recibido.wav')

main(pedir_opcion())