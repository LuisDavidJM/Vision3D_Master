import numpy as np
import binvox_rw
import os

######################### LEER ARCHIVO DE ESQUELETO ORIGINAL ####################################

def leer_binvox(ruta_archivo):
    with open(ruta_archivo, 'rb') as archivo:
        # Se usa la función de binvox para leer el archivo como una matriz 3D
        modelo = binvox_rw.read_as_3d_array(archivo)
    return modelo.data

######################### ELIMINAR RAMAS INECESARIAS ############################################

# Se encuentra los vecinos directos de un punto en el esqueleto
def encontrar_vecinos(punto, esqueleto):
    x, y, z = punto
    vecinos = []
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dz in (-1, 0, 1):
                if dx == dy == dz == 0:
                    continue
                nx, ny, nz = x + dx, y + dy, z + dz
                if 0 <= nx < esqueleto.shape[0] and 0 <= ny < esqueleto.shape[1] and 0 <= nz < esqueleto.shape[2]:
                    if esqueleto[nx, ny, nz]:
                        vecinos.append((nx, ny, nz))
    return vecinos

# Se realiza DFS en el esqueleto para identificar ramas y decide si podarlas
def dfs_podar(esqueleto, punto, visitados, rama_actual, ramas):
    visitados.add(punto)
    rama_actual.append(punto)
    vecinos = encontrar_vecinos(punto, esqueleto)
    
    if len(vecinos) < 2:  
        ramas.append(rama_actual)
        return
    
    for vecino in vecinos:
        if vecino not in visitados:
            dfs_podar(esqueleto, vecino, visitados, rama_actual.copy(), ramas)

# Se identifican y eliminan ramas inecesarias del esqueleto
def podar_ramas(esqueleto, longitud_minima):
    puntos_esqueleto = np.argwhere(esqueleto == 1)
    esqueleto_podado = np.zeros_like(esqueleto)
    visitados = set()
    ramas = []

    for punto in puntos_esqueleto:
        if tuple(punto) not in visitados:
            dfs_podar(esqueleto, tuple(punto), visitados, [], ramas)

    # Se procesan las ramas identificadas y se eliminan las que son más cortas que la longitud mínima
    for rama in ramas:
        if len(rama) >= longitud_minima:
            for punto in rama:
                esqueleto_podado[punto] = 1
    
    return esqueleto_podado

######################### MANEJO DE ARCHIVOS ######################################

def manejo_de_archivos(ruta_rotacion):

    rutas_binvox = f"Objetos3D/EsqueletoORIGINAL/{ruta_rotacion}/"
    nombres_archivos = [f for f in os.listdir(rutas_binvox) if f.endswith('.binvox')]

    # Se crea una lista para almacenar los datos
    resultados = []

    # Ciclo que se encarga de recorrer todos los archivos
    for nombre_archivo in nombres_archivos:
        # Se crea la ruta completa del archivo
        path_completo = os.path.join(rutas_binvox, nombre_archivo)
        esqueleto = leer_binvox(path_completo)

        # Se aplica la poda al esqueleto leido
        longitud_minima_para_podar = 50
        esqueleto_podado = podar_ramas(esqueleto, longitud_minima_para_podar)
        resultados.append(esqueleto_podado)

    ######################### EXPORTAR ESQUELETO A FORMATO SCR ######################################

    ruta_base_e = f"Objetos3D/EsqueletoSCR/{ruta_rotacion}/"
    ruta_base_f = f"Objetos3D/FreemanSCR/{ruta_rotacion}/"

    # Se asegura de que las rutas base existan, si no, se crean
    if not os.path.exists(ruta_base_e):
        os.makedirs(ruta_base_e)

    if not os.path.exists(ruta_base_f):
        os.makedirs(ruta_base_f)

    coodenadas_finales = []

    for idx, resultado in enumerate(resultados):
        # Se convierten los arrays a coordenadas
        converted_coords = binvox_rw.dense_to_sparse(resultado)

        converted_coords_inicio = converted_coords - converted_coords[:, 0][:, np.newaxis]
        
        # Se genera un nombre de archivo unico para cada conjunto de esqueleto
        nombre_archivo_e = f"Esqueleto{ruta_rotacion}-{idx}.scr"
        ruta_archivo_e = os.path.join(ruta_base_e, nombre_archivo_e)
        
        # Se abre y se escribe en el archivo correspondiente
        with open(ruta_archivo_e, "w") as file:
            for i in range(len(converted_coords_inicio[0])):
                x = converted_coords_inicio[0][i]
                y = converted_coords_inicio[1][i]
                z = converted_coords_inicio[2][i]
                file.write("_box\n")
                file.write("C\n")
                file.write(f"{x},{y},{z}\n")
                file.write("C\n")
                file.write("1\n")

        ######################### ORDENAR COORDENADAS ###################################################

        # Se selecciona el punto inicial para comenzar el ordenamiento
        punto_inicio = converted_coords[:, 0]
        ordenado = [punto_inicio]
        indices_a_ordenar = list(range(1, converted_coords.shape[1]))

        while indices_a_ordenar:
            ultimo_punto = ordenado[-1]
            distancias = np.linalg.norm(converted_coords[:, indices_a_ordenar] - ultimo_punto[:, None], axis=0)
            siguiente_idx = indices_a_ordenar[np.argmin(distancias)]
            ordenado.append(converted_coords[:, siguiente_idx])
            indices_a_ordenar.remove(siguiente_idx)

        coordenadas_ordenadas = np.array(ordenado).T

        converted_coords = np.zeros(coordenadas_ordenadas.shape, dtype=np.int16)

        # Se redondean las coordenadas a numeros enteros
        for i in range(coordenadas_ordenadas.shape[1]):
            x = round(coordenadas_ordenadas[0][i])
            y = round(coordenadas_ordenadas[1][i])
            z = round(coordenadas_ordenadas[2][i])
            
            # Se almacenan las coordenadas convertidas
            converted_coords[:, i] = [x, y, z]

        coodenadas_finales.append(converted_coords)

        ######################### EXPORTAR VECTORES FREEMAN DE ESQUELETO #################################

        converted_coords_inicio = converted_coords - converted_coords[:, 0][:, np.newaxis]

        coordenadas = list(zip(converted_coords_inicio[0], converted_coords_inicio[1], converted_coords_inicio[2]))

        # Se genera un nombre de archivo unico para cada conjunto de vectores
        nombre_archivo_f = f"Freeman{ruta_rotacion}-{idx}.scr"
        ruta_archivo_f = os.path.join(ruta_base_f, nombre_archivo_f)

        # Se convierten las coordenadas a lineas en formato CSR
        with open(ruta_archivo_f, "w") as file:
            file.write("_LINE\n")
            # Se itera hasta el penúltimo elemento para comparar con el siguiente
            for i in range(len(coordenadas) - 1):  
                punto_actual = coordenadas[i]
                punto_siguiente = coordenadas[i + 1]
                
                # Se calcula la distancia euclidiana entre el punto actual y el siguiente
                distancia = np.linalg.norm(np.array(punto_actual) - np.array(punto_siguiente))

                # Se escribe el punto actual
                x, y, z = punto_actual
                file.write(f"{x},{y},{z}\n")
                
                # Si la distancia al siguiente punto es mayor que 2, termina la línea actual y comienza una nueva
                if distancia > 2:
                    file.write("\n_LINE\n") 

            x, y, z = coordenadas[-1]
            file.write(f"{x},{y},{z}\n")

        # Se lee el contenido del archivo
        with open(ruta_archivo_f, "r") as file:
            lineas = file.readlines()

        # Se elimina la ultima línea
        lineas = lineas[:-1]

        # Se vuelve a escribir el contenido sin la última linea en el archivo
        with open(ruta_archivo_f, "w") as file:
            file.writelines(lineas)
            file.writelines("\n")

    return coodenadas_finales
