from anytree import AnyNode, RenderTree, PreOrderIter
import numpy as np
import hashlib, secrets
import base64
from collections import Counter
#import chunk

class Codificacion:
    def __init__(self):
        self.codes = {}
        self.binary = np.array([], dtype=tuple)
        self.secret = self.get_secret()
    
    def generarArbolShannon(self, diccionario):
        return self._generarArbol(diccionario, reverse=True)

    def generarArbolHuffman(self, diccionario):
        return self._generarArbol(diccionario, reverse=False)

    def _generarArbol(self, diccionario, reverse):
        diccionario_sort = dict(sorted(diccionario.items(), key=lambda item: item[1], reverse=reverse))
        
        cola = []

        for elemento, frecuencia in diccionario_sort.items():
            nodo = AnyNode(id=elemento,
                        frecuencia=frecuencia,
                            izquierda=None,
                            derecha=None,
                            esHoja=True
                            )
            cola.append(nodo)
        
        while len(cola) > 1:
            
            nodo_izquierda = cola.pop(0)
            nodo_derecha = cola.pop(0)

            nuevo_nodo = AnyNode(
                id = f"{str(nodo_izquierda.frecuencia) + str(nodo_derecha.frecuencia)}",
                frecuencia=nodo_izquierda.frecuencia + nodo_derecha.frecuencia, 
                izquierda = nodo_izquierda, 
                derecha = nodo_derecha,
                esHoja=False
            )

            # Insertar el nuevo nodo en la posición correcta en la cola
            for i in range(len(cola)):
                if nuevo_nodo.frecuencia > cola[i].frecuencia:
                    cola.insert(i, nuevo_nodo)
                    break
            else:
                cola.append(nuevo_nodo)
        
        arbol = cola[0]

        return arbol

    
    def generarCodigos(self, node, bits=""):
        if node.izquierda is not None:
            self.generarCodigos(node.izquierda, bits + '0')
        if node.derecha is not None:
            self.generarCodigos(node.derecha, bits + '1')
        if node.esHoja:
            self.codes[node.id] = bits

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

        return hash_resultado
    
    def agregar_hashes(self, codes):
        nuevo_dict = {self.calcularHash(k,self.secret): (k, v) for k, v in codes.items()}
        return nuevo_dict

    def encoding(self, information, codes):
        for chunk in information:
            #print(chunk)
            self.binary = np.append(self.binary, codes[tuple(chunk)])  # Usar hash_chunk como clave
        #print('Info in binary:', self.binary)
        return self.binary


    def decoding(self, codes, binary):
        decode_text = []
        reverse_codes = {v: k for k, v in codes.items()}  # Invertir el diccionario 'codes'
        for bit in binary:
            if bit in reverse_codes:
                decode_text.append(reverse_codes[bit])  # Agregar el valor decodificado a 'decode_text'
        return np.array(decode_text)  # Convertir la lista a un arreglo de NumPy
    
    def encode_numpy_array_to_base64(self, arr):
        # Convertir el arreglo a bytes
        arr_bytes = arr.tobytes()
        # Codificar los bytes a base64
        base64_bytes = base64.b64encode(arr_bytes)
        # Convertir los bytes a string
        base64_string = base64_bytes.decode()
        return base64_string

    def encriptarB64(self, information):
        information_hash = []
        print(information.pop())
        for chunk in information:
            chunk_b64 = self.encode_numpy_array_to_base64(chunk)
            hash_chunk = self.calcularHash(chunk_b64, self.secret)
            information_hash.append(hash_chunk)
            #print(hash_chunk)
        return information_hash
    
    def tuple_to_base64(self, t):
        # Convertir la tupla a un arreglo de NumPy
        arr = np.array(t)
        # Convertir el arreglo de NumPy a bytes
        arr_bytes = arr.tobytes()
        # Codificar los bytes a base64
        base64_bytes = base64.b64encode(arr_bytes)
        # Convertir los bytes a string
        base64_string = base64_bytes.decode()
        return base64_string

    def handshakeB64(self, diccionario):
        for arr in diccionario:
            #print(arr)
            # Codificar la clave a base64 y usarla como el nuevo valor
            diccionario[arr] = self.tuple_to_base64(arr)
        return diccionario
    
    def busqueda_binaria(self, lista, elem):
        izquierda, derecha = 0, len(lista) - 1
        while izquierda <= derecha:
            medio = (izquierda + derecha) // 2
            if lista[medio] < elem:
                izquierda = medio + 1
            elif lista[medio] > elem:
                derecha = medio - 1
            else:
                return medio
        return -1

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

    def decodingB642(self, handshake, codificado):
        decode_text = []
        reverse_codes = {v: k for k, v in handshake.items()}
        nuevo_dict = {self.calcularHash(k, self.secret): v for k, v in reverse_codes.items()}
        for elem in codificado:
            if elem in nuevo_dict:
                decode_text.append(nuevo_dict[elem])
        return np.array(decode_text)
    
    def encriptarRLL(self, information):
        def run_length_encoding(input_string):
            count = 1
            prev = ""
            lst = []
            for character in input_string:
                if character != prev:
                    if prev:
                        entry = (prev,count)
                        lst.append(entry)
                    count = 1
                    prev = character
                else:
                    count += 1
            else:
                entry = (character,count)
                lst.append(entry)
            return lst

        # Convertir los arrays de NumPy a cadenas
        string_information = [''.join(map(str, np_array)) for np_array in information]
        # Calcular la frecuencia de cada array en la lista
        frequency = Counter(string_information)
        # Aplicar la compresión RLL a las frecuencias
        compressed = run_length_encoding(''.join(frequency.elements()))
        return compressed

    def decodificarRLL(self, compressed):
        # Inicializar una lista vacía para almacenar los arrays decodificados
        decoded = []

        # Iterar sobre cada tupla en la lista comprimida
        for array_string, count in compressed:
            # Convertir la cadena a un array de NumPy
            numpy_array = np.array([int(char) for char in array_string])

            # Añadir el array a la lista 'decoded' el número de veces especificado por 'count'
            for _ in range(count):
                decoded.append(numpy_array)

        return decoded

    def get_codes(self):
        return self.codes
    
    def get_secret(self):
        with open('scripts/SecretKey.txt', 'r') as archivo:
    # Leer el contenido del archivo y almacenarlo en un string
            contenido = archivo.read()
        return contenido