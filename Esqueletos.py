import numpy as np
import binvox_rw
import os

# Se abre el archivo .binvox para lectura en modo binario
def leer_binvox(ruta_archivo):
    with open(ruta_archivo, 'rb') as archivo:
        # Se usa la función de binvox para leer el archivo como una matriz 3D
        modelo = binvox_rw.read_as_coord_array(archivo)
    return modelo

#np.set_printoptions(threshold=np.inf)

ruta_binvox = "../Objetos3D/ArchivosEsqueletoORIGINAL/256x256x256-5E.binvox"
esqueleto = leer_binvox(ruta_binvox)

# # Un punto de inicio hipotético, elige uno que tenga sentido para tu esqueleto
# punto_inicio = esqueleto.data[:, 0]
# ordenado = [punto_inicio]
# indices_a_ordenar = list(range(1, esqueleto.data.shape[1]))

# while indices_a_ordenar:
#     ultimo_punto = ordenado[-1]
#     distancias = np.linalg.norm(esqueleto.data[:, indices_a_ordenar] - ultimo_punto[:, None], axis=0)
#     siguiente_idx = indices_a_ordenar[np.argmin(distancias)]
#     ordenado.append(esqueleto.data[:, siguiente_idx])
#     indices_a_ordenar.remove(siguiente_idx)

# coordenadas_ordenadas = np.array(ordenado).T

# converted_coords = np.zeros(coordenadas_ordenadas.shape, dtype=np.int16)

# for i in range(coordenadas_ordenadas.shape[1]):  # Asumiendo que esqueleto.data tiene la forma (3, N)
#     x = round(coordenadas_ordenadas[0][i])
#     y = round(coordenadas_ordenadas[1][i])
#     z = round(coordenadas_ordenadas[2][i])
    
#     # Almacenar las coordenadas convertidas
#     converted_coords[:, i] = [x, y, z]

#     #print(f"{x},{y},{z}")

# # Convertir coordenadas a lineas en formato CSR
# with open("../Objetos3D/Pruebas/freeman-ordenado.scr","w") as file:
#     file.write("3DPOL\n")
#     for i in range(len(converted_coords[0])):
#         x = converted_coords[0][i]
#         y = converted_coords[1][i]
#         z = converted_coords[2][i]
#         file.write(f"{x},{y},{z}\n")

converted_coords = np.zeros(esqueleto.data.shape, dtype=np.int16)

for i in range(esqueleto.data.shape[1]):  # Asumiendo que esqueleto.data tiene la forma (3, N)
    x = esqueleto.data[0][i]
    y = esqueleto.data[1][i]
    z = esqueleto.data[2][i]
    
    # Almacenar las coordenadas convertidas
    converted_coords[:, i] = [x, y, z]

# Convertir coordenadas a voxeles en formato CSR
with open("../Objetos3D/Pruebas/esqueleto.scr","w") as file:
    for i in range(len(converted_coords[0])):
        x = converted_coords[0][i]
        y = converted_coords[1][i]
        z = converted_coords[2][i]
        file.write("_box\n")
        file.write("C\n")
        file.write(f"{x},{y},{z}\n")
        file.write("C\n")
        file.write("1\n")

# Convertir coordenadas a lineas en formato CSR
with open("../Objetos3D/Pruebas/freeman.scr","w") as file:
    file.write("3DPOL\n")
    for i in range(len(converted_coords[0])):
        x = converted_coords[0][i]
        y = converted_coords[1][i]
        z = converted_coords[2][i]
        file.write(f"{x},{y},{z}\n")
        print(f"{x},{y},{z}")


