import numpy as np
import binvox_rw
import os

# Se abre el archivo .binvox para lectura en modo binario
def leer_binvox(ruta_archivo):
    with open(ruta_archivo, 'rb') as archivo:
        # Se usa la función de binvox para leer el archivo como una matriz 3D
        modelo = binvox_rw.read_as_3d_array(archivo)
    return modelo.data

def encontrar_vecinos(punto, esqueleto):
    """Encuentra los vecinos directos de un punto en el esqueleto."""
    x, y, z = punto
    vecinos = []
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dz in (-1, 0, 1):
                if dx == dy == dz == 0:
                    continue  # Ignora el punto actual
                nx, ny, nz = x + dx, y + dy, z + dz
                if 0 <= nx < esqueleto.shape[0] and 0 <= ny < esqueleto.shape[1] and 0 <= nz < esqueleto.shape[2]:
                    if esqueleto[nx, ny, nz]:
                        vecinos.append((nx, ny, nz))
    return vecinos

def dfs_podar(esqueleto, punto, visitados, rama_actual, ramas):
    """Realiza DFS en el esqueleto para identificar ramas y decide si podarlas."""
    visitados.add(punto)
    rama_actual.append(punto)
    vecinos = encontrar_vecinos(punto, esqueleto)
    
    if len(vecinos) < 2:  # Punto de inicio/final de una rama o punto aislado
        ramas.append(rama_actual)
        return
    
    for vecino in vecinos:
        if vecino not in visitados:
            dfs_podar(esqueleto, vecino, visitados, rama_actual.copy(), ramas)

def podar_ramas(esqueleto, longitud_minima):
    """Identifica y elimina ramas del esqueleto basado en una longitud mínima."""
    puntos_esqueleto = np.argwhere(esqueleto == 1)
    esqueleto_podado = np.zeros_like(esqueleto)
    visitados = set()
    ramas = []

    for punto in puntos_esqueleto:
        if tuple(punto) not in visitados:
            dfs_podar(esqueleto, tuple(punto), visitados, [], ramas)

    # Procesar las ramas identificadas y eliminar las que son más cortas que la longitud mínima
    for rama in ramas:
        if len(rama) >= longitud_minima:
            for punto in rama:
                esqueleto_podado[punto] = 1
    
    return esqueleto_podado

ruta_binvox = "../Objetos3D/ArchivosEsqueletoORIGINAL/128x128x128-1E.binvox"
esqueleto = leer_binvox(ruta_binvox)

# Aplica la poda al esqueleto leído
longitud_minima_para_podar = 100
esqueleto_podado = podar_ramas(esqueleto, longitud_minima_para_podar)

nombre_archivo_salida1 = '../Objetos3D/Pruebas/esqueleto.npy'
np.save(nombre_archivo_salida1, esqueleto)

nombre_archivo_salida2 = '../Objetos3D/Pruebas/esqueleto_podado.npy'
np.save(nombre_archivo_salida2, esqueleto_podado)