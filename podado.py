import numpy as np
import binvox_rw
import os

# Se abre el archivo .binvox para lectura en modo binario
def leer_binvox(ruta_archivo):
    with open(ruta_archivo, 'rb') as archivo:
        # Se usa la función de binvox para leer el archivo como una matriz 3D
        modelo = binvox_rw.read_as_coord_array(archivo)
    return modelo


np.set_printoptions(threshold=np.inf)

ruta_binvox = "../Objetos3D/ArchivosEsqueletoORIGINAL/128x128x128-1E.binvox"
esqueleto = leer_binvox(ruta_binvox)


converted_coords = np.zeros(esqueleto.data.shape, dtype=np.float64)

# Iterar a través de cada conjunto de coordenadas en esqueleto.data
for i in range(esqueleto.data.shape[1]):  # Asumiendo que esqueleto.data tiene la forma (3, N)
    x_n = (esqueleto.data[0][i] + 0.5) / esqueleto.dims[0]
    y_n = (esqueleto.data[1][i] + 0.5) / esqueleto.dims[1]
    z_n = (esqueleto.data[2][i] + 0.5) / esqueleto.dims[2]
    
    # Aplicar la escala y traslación
    x = esqueleto.scale * x_n + esqueleto.translate[0]
    y = esqueleto.scale * y_n + esqueleto.translate[1]
    z = esqueleto.scale * z_n + esqueleto.translate[2]
    
    # Almacenar las coordenadas convertidas
    converted_coords[:, i] = [x, y, z]

#print(esqueleto.translate)

#print(esqueleto.data[0][0], esqueleto.data[1][0], esqueleto.data[2][0])
#print(x, y, z)
    
out = binvox_rw.sparse_to_dense(converted_coords, esqueleto.dims)

nombre_archivo_salida1 = '../Objetos3D/Pruebas/esqueleto_coo.npy'
np.save(nombre_archivo_salida1, out)
    
print(converted_coords)
