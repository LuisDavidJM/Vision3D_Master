import numpy as np
import Esqueletos
from DiccionarioF16 import diccionario_f26

def buscar_letras(coordenadas_array):
    letras = []
    # Utiliza numpy para transponer el array 3xN y obtener tuplas de coordenadas (x, y, z)
    coordenadas_transpuestas = np.transpose(coordenadas_array)

    for coordenada in coordenadas_transpuestas:
        # Convierte la tupla de numpy a una tupla de Python para que coincida con las claves del diccionario
        coordenada_tupla = tuple(coordenada)
        if coordenada_tupla in diccionario_f26:
            letras.append(diccionario_f26[coordenada_tupla])
        else:
            letras.append('?')  # Si no encuentra la coordenada, agrega un signo de interrogación
    return letras

# Ejemplo de uso con el array de coordenadas proporcionado convertido a un array de numpy
coordenadas_array_np = np.array([
    [1, 0, -1, 1],  # x
    [0, 1, 0, -1],  # y
    [0, 1, -1, 1],  # z
])

letras_encontradas = buscar_letras(coordenadas_array_np)
#print(letras_encontradas)


ruta_rotacion = ["Original", "Rotado15", "Rotado25", "Rotado45", "Rotado75"]

# Coordenadas de los 10 esqueletos originales y cada rotación
out = Esqueletos.manejo_de_archivos(ruta_rotacion[0])
# out_15 = Esqueletos.manejo_de_archivos(ruta_rotacion[1])
# out_25 = Esqueletos.manejo_de_archivos(ruta_rotacion[2])
# out_45 = Esqueletos.manejo_de_archivos(ruta_rotacion[3])
# out_75 = Esqueletos.manejo_de_archivos(ruta_rotacion[4])

np.set_printoptions(threshold=np.inf)
#print(out[0])

out_inicio = out[0] - out[0][:, 0][:, np.newaxis]
#print(out_inicio)

# Calcular las diferencias entre puntos adyacentes
diferencias = np.diff(out[0], axis=1)

# Calcular la distancia Euclidiana para cada par de puntos adyacentes
distancias = np.sqrt(np.sum(diferencias**2, axis=0))

# Inicializar el índice de inicio del segmento actual
inicio = 0

# Lista para almacenar los arrays resultantes
arrays_resultantes = []

# Iterar sobre cada distancia y verificar la condición
for i, distancia in enumerate(distancias, start=1):
    if distancia > 2:
        # Si la distancia es mayor a 2, extraer el segmento actual y agregarlo a la lista
        segmento = out[0][:, inicio:i]
        arrays_resultantes.append(segmento)
        inicio = i  # Actualizar el índice de inicio para el próximo segmento

# No olvidar agregar el último segmento después del último salto encontrado
if inicio < out[0].shape[1]:
    segmento_final = out[0][:, inicio:]
    arrays_resultantes.append(segmento_final)

# Mostrar los arrays resultantes
for i, array in enumerate(arrays_resultantes, start=1):
    print(f"Array {i}:")
    print(array)
    print()  # Línea en blanco para separar los arrays


