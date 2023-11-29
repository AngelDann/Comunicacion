
from WalkieTalkie import WalkieTalkie
from Canal import Canal
import random

def pedir_opcion():
    opciones = ['Sin codificar', 'Huffman', 'Shannon','Base64','RLL']
    while True:
        print("Por favor, elige una opción:")
        for i, opcion in enumerate(opciones, 0):
            print(f"{i}. {opcion}")
        eleccion = input("Ingresa el número de tu opción: ")
        if eleccion in ['0', '1', '2','3', '4']:
            return int(eleccion)
        else:
            print("Entrada inválida. Por favor, ingresa un número del 0 al 3.")

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
    #El valor de codificado lo sue para pruebas pero no se usa
    #Se usa la lista_canales con los paquetes para ordenarlos y transfromarlo de vuelta a la original
    rate,señal_modulada, codificado, handshake = walkie1.BotonTransmitir(rate,audio_data)

    #Canal
    print(opcion)
    canal = Canal(walkie1, walkie2)
    print("Atenuacion:", canal.get_atenuacion())
    lista_canales = canal.pasoInformacion(rate, señal_modulada, codificado, opcion=opcion)

    # Recepción
    walkie2.BotonRecibir('./scripts/audios/audio_modulado_ruido.wav', codificado, handshake, lista_canales)

    #Destino Final
    #walkie2.reproducir('scripts/audios/audio_recibido.wav')

main(pedir_opcion())