from DiccionarioF16 import diccionario_f26
from Coordenadas import ajuste_coordenadas
import numpy as np
import Esqueletos

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

coord = ajuste_coordenadas(out[3])

# Mostrar los segmentos ajustados
for i, seg in enumerate(coord, start=1):
    print(f"Segmento {i}:")
    print(seg)
    print()