from anytree import AnyNode, RenderTree, PreOrderIter
import numpy as np

class Huffman:
    def __init__(self):
        self.codes = {}
        self.binary = np.array([], dtype=tuple)
    
    def generarArbol(self, diccionario):
        diccionario_sort = dict(sorted(diccionario.items(), key=lambda item: item[1]))
        
        cola = []

        for elemento, frecuencia in diccionario_sort.items():
            nodo = AnyNode(id=elemento,
                           frecuencia=frecuencia,
                            izquierda=None,
                            derecha=None,
                            esHoja=True
                            )
            cola.append(nodo)
        
        i = 0
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

            cola.append(nuevo_nodo)
            i+=1
        
        arbol_huffman = cola[0]

        return arbol_huffman
    
    def huffman_codes(self, node, bits=""):
        if node.izquierda is not None:
            self.huffman_codes(node.izquierda, bits + '0')
        if node.derecha is not None:
            self.huffman_codes(node.derecha, bits + '1')
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
