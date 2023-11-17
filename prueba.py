
import numpy as np
import hashlib

informacion = [np.array([ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  9.,  0., -9.,  0.,  0.,  0.,  0.,  0.,  0.,
                            0.,  0.,  0., -9.,  0.,  0., -9.,  0.,  0., -9.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
                            0.,  0.,  0.,  0.,  0.,  9.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
                            0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  9.,  0.,  0.,  0.,
                            0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  9.,  0.,  0.,
                            0.,  0.,  9.,  9.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  9.,
                            0.,  0.,  0.,  9.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
                            0.,  0.,  0.,  9.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
                            0.,  0.,  0.,  9.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
                            0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
                            0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
                            0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
                            0.,  0.,  0.,  0.,  9.,  9.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
                            0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
                            0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
                            0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
                            0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
                            0.,  0.,  0.,  0.,  0.,  0.])]

# Convertir la información a un numpy array
informacion = np.array(informacion)

# Tu palabra secreta
palabra_secreta = 'palabra_secreta'

# Convertir la información a bytes
informacion_bytes = informacion.tobytes()

# Crear el objeto SHA256
hash_obj = hashlib.sha256()

# Actualizar el objeto SHA256 con la palabra secreta y la información
hash_obj.update(palabra_secreta.encode('utf-8'))
hash_obj.update(informacion_bytes)

# Obtener el hash
hash_resultado = hash_obj.hexdigest()
print(hash_resultado)