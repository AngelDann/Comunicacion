# Esquema-comunicacion
Respositorio para la revision del esquema de comunicación
Se tienen 2 codificaciones y la modulacion adaptativa

## Esquema de comunicacion walkir-talkie

* Fuente de información: Voz de una persona.
* Transmisor: El walkie-talkie que toma la voz de la persona, la transforma en señal eléctrica conviertiendola en una onda. Hace un producto de esa con la onda portadora creando así la onda de amplitud modulada (AM).
* Ruido: La distancia a la que se encuentran las personas usando las radios.
* Canal: Aire
* Receptor: El segundo walkie-talkie que toma la señal, quita la onda portadora y se queda con la onda de informacion.
* Destino: el Walkie-takie reproduce la información que recibe.

## Proceso
El proceso que sigue el codigo para simular la comunicacion es el siguiente:
* Primero se le pregunta al usuario si quiere hacer la comunicacion con alguna codificacion o sin codificacion.
* Se crean los WalkieTalkies con sus parametros (solo es relevante saber la opcion que manejan)

**Sin codificacion**

1.- El WalkieTalkie crea la Fuente de Informacion que es el audio alarma.wav y lo transforma a un arreglo mono.
  
2.- El WalkieTalkie transmite la informaicon y devuelve las variables rate, señal_modulada.

3.- El canal usa la señal modulada para pasarlo por segmentos y agregar ruido (que es multiplicarlo) con un 6% de probabilidad en cada segmento.

4.- El canal guarda este nuevo audio modulado con ruido.

5.- El receptor toma el audio con ruido, lo desmoluda y finalmente obtiene la información original que guarda en otro archivo.

**Con codificacion**

1.- El WalkieTalkie crea la Fuente de Informacion que es el audio alarma.wav y lo transforma a un arreglo mono.

2.- El WalkieTalkie transmite la informacion según la opción que se eligió, si es Huffman devolverá la información codificada y su handshake para poder descodificarlo.

3.- El canal usa la modulación adaptativa para poder transmitir los datos a través de distintos canales que tienen una probabilidad de generar ruido distinta.

>self.canales = [[] for _ in range(5)] #Canales en total

>self.probabilidades_ruido = [0.7, 0.2, 0.1, 0.4, 0.8] #La probabilidad de ruido que tiene cada canal

4.- Laa modulación adaptativa ocurre cuando se identifica que hay ruido en ese canal y luego se cambia a otro para poder guardar la información.
```
            if self.agregarRuidoEnCodificado(probabilidad=self.probabilidades_ruido[j]):
                codificado = np.delete(codificado, i)
                if j < len(self.canales)-1:
                    j+=1 #Cambio de canal a otro que no tenga ruido
                    self.canales[j].append((i, elem))
                else:
                    j = 0
                    self.canales[j].append((i, elem))
            else:
                self.canales[j].append((i, elem)) #Sigue en el mismo canal
                i += 1

```
![image](https://github.com/AngelDann/Comunicacion/assets/147886154/ecaf79a7-59ec-434e-877b-f00ef5925355)

5.- El Receptor se encarga de tomar estos canales, ordenar la información a como estaba originalmente

```
# Demodulación
            lista_plana = [tupla for sublista in lista_canales for tupla in sublista]
            lista_plana.sort(key=lambda tupla: tupla[0])
            lista_final = [tupla[1] for tupla in lista_plana]
            señal_modulada_mono_decodificada = self.codificacion.decoding(handshake, lista_final)
            #Como esta dividido se tiene que volver a hacer unidimensional
            señal_demodulada = señal_modulada_mono_decodificada.flatten() / portadora

```
6.- Y finalmente la informacion se guarda en el archivo.
````
        # Conversión a valores originales
        audio_data_original = np.round(señal_demodulada).astype(np.int16)

        # Creación de señal estéreo
        audio_data_original_stereo = np.column_stack((audio_data_original, audio_data_original))

        #Se guarda el archivo de audio
        self.guardar_audio('./scripts/audios/audio_recibido.wav', rate_received, audio_data_original_stereo)

````

## Codigo
El codigo tiene 2 tipo de codificaciones y la modulacion adaptativa.

### Comunicacion
Este codigo es el principal donde se simula la comunicacion. Se le pide al usuario que seleccione alguna codificacion para que comience el proceso.

![image](https://github.com/AngelDann/Comunicacion/assets/147886154/3077c0e4-0d70-482d-8981-0f08ae9586b7)

### Clase codificacion
Contiene dos tiposs de codificaciones funcionales:
* Huffman
* Shannon Fanno
El proceso que sigue es formar un arbol binario a partir de un diccionario de frecuencias que genera el Transmisor, tambien tiene funcion llamada "generarCodigos" para hacer el diccionario que se usa como handshake para que el Receptor pueda desencriptar la informacion.

### Clase WalkieTalkie
Esta clase cuenta con funciones tanto de transmisión como de recepción. La idea es crear 2 objetos donde uno haga de Transmisor y otro de Receptor.
El transmisor actua segun la opcion que haya seleccionado el usuario. Si seleccionó sin codificacion entonces el proceso se hará normal a traves del canal.
En el caso que el usuario seleccione Huffman o Shannon se hará la codificacion y se mandará la información codificada a través del canal.


