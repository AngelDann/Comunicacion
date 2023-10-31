import numpy as np
from Huffman import Huffman 
from Shannon import Shannon
from anytree import AnyNode, RenderTree, PreOrderIter    

from Codificacion import Codificacion

codificacion = Codificacion()
huffman = Huffman()
shannon = Shannon()
##########################################################
        # Supongamos que tienes una matriz NumPy
# Ejemplo de uso
mi_matriz = np.array([[1, 2, 3],
                      [1, 2, 3],
                      [4, 5, 6],
                      [4, 5, 6],
                      [1, 2, 3],
                      [7, 8, 9]])



codigo_aritmetico = codificacion.codificacionAritmetica(mi_matriz)
print(codigo_aritmetico)

array_vacio = [[] for _ in range(5)]

print(array_vacio[5])

