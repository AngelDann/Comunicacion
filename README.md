# Esquema-comunicacion
Respositorio para la revision del esquema de comunicación
Se tienen 2 codificaciones y la modulacion adaptativa

## Esquema de comunicacion walkie-talkie

* Fuente de información: Voz de una persona.
* Transmisor: El walkie-talkie que toma la voz de la persona, la transforma en señal eléctrica conviertiendola en una onda. Hace un producto de esa con la onda portadora creando así la onda de amplitud modulada (AM).
* Ruido: La distancia a la que se encuentran las personas usando las radios.
* Canal: Aire
* Receptor: El segundo walkie-talkie que toma la señal, quita la onda portadora y se queda con la onda de informacion.
* Destino: el Walkie-takie reproduce la información que recibe.

## Proceso con Hash
El tipo de codificación que tiene el hasheo es la que se hace con base64.
* Codificar informacion

Lo que se hace es que cada paquete de la información se transforma a una codifiacion base64, luego se hace el hasheo de la información usando la palabra secreta que está en el archivo SecretKey.txt. Finalmente todo se guarda en information_hash y se retorna.

```
    def encriptarB64(self, information):
        information_hash = []
        for chunk in information:
            chunk_b64 = self.encode_numpy_array_to_base64(chunk)
            hash_chunk = self.calcularHash(chunk_b64, self.secret)
            information_hash.append(hash_chunk)
        return information_hash

    def calcularHash(self, chunk, palabra_secreta):
        # Convertir la información a un numpy array
        chunk = np.array(chunk)
        # Convertir la información a bytes
        chunk_bytes = chunk.tobytes()
        #Se hace el objeto hash con la palabra secreta
        hash_obj = hashlib.sha256()
        hash_obj.update(palabra_secreta.encode('utf-8'))
        hash_obj.update(chunk_bytes)
        # Obtener el hash
        hash_resultado = hash_obj.hexdigest()
```
En este caso para el handshake se usa el diccionario de frecuencias y se cambia las frecuencias por la información original en base64. Este es el handshake que se manda al Receptor:

```
    def handshakeB64(self, diccionario):
        for arr in diccionario:
            # Codificar la clave a base64 y usarla como el nuevo valor
            diccionario[arr] = self.tuple_to_base64(arr)
        return diccionario
```
Estructura del handshake:
```
{
  informacion_original : informacion_base64
}
```

* Decodificar información

Para regresar la información a su estado original lo que se hace es hashear la información que está en base64 del handshake:
```
reverse_codes = {v: k for k, v in handshake.items()}

{
  informacion_original : informacion_hash
}
```
Luego se invierten las keys porque vamos a usar el hash para encontrar la información original:
```
nuevo_dict = {self.calcularHash(k, self.secret): v for k, v in reverse_codes.items()}

{
  informacion_hash : informacion_original 
}
```
Y cuando está listo se hace lo necesario para usar la búsqueda binaria, encontrar el valor original y agregarlo a una lista con toda la información original.
```
    def decodingB64(self, handshake, codificado):
        decode_text = []
        reverse_codes = {v: k for k, v in handshake.items()}
        nuevo_dict = {self.calcularHash(k, self.secret): v for k, v in reverse_codes.items()}
        keys_list = sorted(nuevo_dict.keys())
        for elem in codificado:
            indice = self.busqueda_binaria(keys_list, elem)
            if indice != -1:
                decode_text.append(nuevo_dict[keys_list[indice]])
        return np.array(decode_text)
```

* Extra

Como ya se está usando un diccionario es incluso más rápido y sencillo usar el mismo diccionario y la clave para encontrar el hash, siempre y cuando no se use el salt.
```
    def decodingB64_2(self, handshake, codificado):
        decode_text = []
        reverse_codes = {v: k for k, v in handshake.items()}
        nuevo_dict = {self.calcularHash(k, self.secret): v for k, v in reverse_codes.items()}
        for elem in codificado:
            if elem in nuevo_dict:
                decode_text.append(nuevo_dict[elem])
        return np.array(decode_text)
```

## Codigo
El codigo tiene 3 tipos de codificaciones y la modulacion adaptativa.

### Comunicacion
Este codigo es el principal donde se simula la comunicacion. Se le pide al usuario que seleccione alguna codificacion para que comience el proceso.

![image](https://github.com/AngelDann/Comunicacion/assets/147886154/14b29963-6b5d-4890-8217-a80abb575579)

### Clase codificacion
Contiene tres tiposs de codificaciones funcionales:
* Huffman
* Shannon Fanno
* Base64
El proceso que sigue es formar un arbol binario a partir de un diccionario de frecuencias que genera el Transmisor, tambien tiene funcion llamada "generarCodigos" para hacer el diccionario que se usa como handshake para que el Receptor pueda desencriptar la informacion.

### Clase WalkieTalkie
Esta clase cuenta con funciones tanto de transmisión como de recepción. La idea es crear 2 objetos donde uno haga de Transmisor y otro de Receptor.
El transmisor actua segun la opcion que haya seleccionado el usuario. Si seleccionó sin codificacion entonces el proceso se hará normal a traves del canal.
En el caso que el usuario seleccione Huffman o Shannon se hará la codificacion y se mandará la información codificada a través del canal.


