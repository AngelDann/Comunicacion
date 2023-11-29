import uuid
import numpy as np
import hashlib, secrets
import hmac

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
informacion2 = [np.array([ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  9.,  0., -9.,  0.,  0.,  0.,  0.,  0.,  0.,
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
# Tu palabra secreta
palabra_secreta = 'palabra_secreta'

# Convertir la información a un numpy array
informacion = np.array(informacion)
informacion2 = np.array(informacion2)

# Convertir la información a bytes
informacion_bytes = informacion.tobytes()
informacion_bytes2 = informacion2.tobytes()

# Crear el salt para el primer hash
salt1 = uuid.uuid4().hex

# Crear el objeto HMAC para el primer hash
hmac_obj = hmac.new((palabra_secreta + salt1).encode(), informacion_bytes, hashlib.sha256)

# Obtener el hash para el primer conjunto de datos
hash_resultado = hmac_obj.hexdigest()

# Crear el salt para el segundo hash
salt2 = uuid.uuid4().hex

# Crear el objeto HMAC para el segundo hash
hmac_obj2 = hmac.new((palabra_secreta + salt2).encode(), informacion_bytes2, hashlib.sha256)

# Obtener el hash para el segundo conjunto de datos
hash_resultado2 = hmac_obj2.hexdigest()

# Almacenar el hash y el salt
hash_y_salt1 = hash_resultado + ':' + salt1
hash_y_salt2 = hash_resultado2 + ':' + salt2

# Extraer el salt del hash almacenado
salt_almacenado1 = hash_y_salt1.split(':')[1]
salt_almacenado2 = hash_y_salt2.split(':')[1]

# Generar un nuevo hash a partir de los datos que estás verificando, utilizando el salt almacenado
hmac_obj_verificacion1 = hmac.new((palabra_secreta + salt_almacenado1).encode(), informacion_bytes, hashlib.sha256)
hmac_obj_verificacion2 = hmac.new((palabra_secreta + salt_almacenado2).encode(), informacion_bytes2, hashlib.sha256)

# Obtener el hash de verificación
hash_verificacion1 = hmac_obj_verificacion1.hexdigest()
hash_verificacion2 = hmac_obj_verificacion2.hexdigest()

# Comparar el hash de verificación con el hash almacenado
print(secrets.compare_digest(hash_verificacion1, hash_resultado))
print(secrets.compare_digest(hash_verificacion2, hash_resultado2))