from anytree import AnyNode, RenderTree, PreOrderIter
import numpy as np

class Codificacion:
    def __init__(self):
        self.codes = {}
        self.binary = np.array([], dtype=tuple)
    
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

    def encoding(self, information, codes):
        for chunk in information:
            #print(chunk)
            self.binary = np.append(self.binary, codes[tuple(chunk)])
        #print('Info in binary:', self.binary)
        return self.binary


    def decoding(self, codes, binary):
        decode_text = []
        reverse_codes = {v: k for k, v in codes.items()}  # Invertir el diccionario 'codes'
        for bit in binary:
            if bit in reverse_codes:
                decode_text.append(reverse_codes[bit])  # Agregar el valor decodificado a 'decode_text'
        return np.array(decode_text)  # Convertir la lista a un arreglo de NumPy

    def get_codes(self):
        return self.codes
    
    def codificacionAritmetica(self, matriz):
        # Inicializar los límites inferior y superior
        lower_bound = 0
        upper_bound = 1

        # Iterar a través de cada elemento en la matriz
        for elemento in np.nditer(matriz):
            # Convertir el elemento a un tipo inmutable (tupla o número)
            elemento = elemento.item() if elemento.size == 1 else tuple(elemento)
            
            if elemento in self.codes:
                rango = upper_bound - lower_bound
                upper_bound = lower_bound + rango * self.codes[elemento][1]
                lower_bound = lower_bound + rango * self.codes[elemento][0]
            else:
                print(f"Elemento {elemento} no encontrado en los códigos.")

        # El código aritmético es cualquier número en el intervalo [lower_bound, upper_bound)
        codigo_aritmetico = lower_bound

        return codigo_aritmetico


    def decodificacionAritmetica(self, codigo, longitud):
        # Inicializar los límites inferior y superior
        lower_bound = 0
        upper_bound = 1

        # Inicializar la matriz decodificada
        matriz_decodificada = np.empty(longitud)

        # Iterar a través de cada posición en la matriz decodificada
        for i in range(longitud):
            rango = upper_bound - lower_bound

            # Encontrar el símbolo cuyo intervalo incluye el código aritmético
            for simbolo, (lower, upper) in self.codes.items():
                if lower <= codigo < upper:
                    matriz_decodificada[i] = simbolo

                    # Actualizar los límites inferior y superior
                    upper_bound = lower_bound + rango * upper
                    lower_bound = lower_bound + rango * lower

                    # Eliminar la parte del código que ya hemos decodificado
                    codigo = (codigo - lower) / (upper - lower)

                    break

        return matriz_decodificada