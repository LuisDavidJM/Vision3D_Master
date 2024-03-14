import numpy as np
import os

# Función para calcular la distancia Euclidiana entre dos puntos
def distancia_euclidiana(punto1, punto2):
    return np.sqrt(np.sum((punto1 - punto2) ** 2))

# Función para verificar si alguna distancia es menor a 2
def existe_distancia_menor_a_2(punto, otros_arrays):
    for array in otros_arrays:
        for coordenada in array.T:  # .T para iterar sobre columnas (puntos)
            if distancia_euclidiana(punto, coordenada) < 2:
                return True
    return False

# Función auxiliar para calcular la distancia Euclidiana entre dos puntos
def distancia_euclidiana_mod(p1, p2):
    return np.linalg.norm(p1 - p2)


def ajuste_coordenadas(out, ruta_rotacion, idx):
    ######################### AJUSTAR COORDENADAS ###################################################

    out_inicio = out - out[:, 0][:, np.newaxis]

    ######################### IDENTIFICAR LAS RAMAS ###################################################

    # Se calcula las diferencias entre puntos adyacentes
    diferencias = np.diff(out_inicio, axis=1)

    # Se calcula la distancia euclidiana para cada par de puntos adyacentes
    distancias = np.sqrt(np.sum(diferencias**2, axis=0))
    inicio = 0

    # Lista para almacenar los arrays resultantes
    arrays_resultantes = []

    # Se itera sobre cada distancia y se verificar la condición
    for i, distancia in enumerate(distancias, start=1):
        # Si la distancia es mayor a 2, se extrae el segmento actual y se agrega a la lista
        if distancia > 2:
            segmento = out_inicio[:, inicio:i]
            arrays_resultantes.append(segmento)
            inicio = i

    # Se agrega el ultimo segmento despues del ultimo salto encontrado
    if inicio < out_inicio.shape[1]:
        segmento_final = out_inicio[:, inicio:]
        arrays_resultantes.append(segmento_final)

    # Se separan los segmentos en dos listas basadas en su longitud
    segmentos_largos = [seg for seg in arrays_resultantes if seg.shape[1] > 15]
    segmentos_cortos = [seg for seg in arrays_resultantes if seg.shape[1] <= 15]

    ######################### ACOMODAR LAS RAMAS ###################################################

    # Se itera sobre los arrays resultantes, modificando los necesarios
    for i in range(1, len(segmentos_largos)):  
        primer_punto = segmentos_largos[i][:, 0] 
        otros_arrays = segmentos_largos[:i] + segmentos_largos[i+1:]
        
        # Se verifica si existe alguna distancia menor a 2
        if not existe_distancia_menor_a_2(primer_punto, otros_arrays):
            # Se invierte el array actual si no hay distancias menores a 2
            segmentos_largos[i] = np.flip(segmentos_largos[i], axis=1)

    arrays_resultantes_final = segmentos_largos + segmentos_cortos

    ######################### AJUSTES PARA CODIFICAR ###################################################

    # Se prepara un nuevo contenedor para los segmentos ajustados
    segmentos_ajustados = [arrays_resultantes_final[0]]

    # Se procesa cada segmento a partir del segundo
    for i in range(1, len(arrays_resultantes_final)):
        segmento_actual = arrays_resultantes_final[i]
        punto_mas_cercano = None
        distancia_minima = np.inf
        
        primer_punto_actual = segmento_actual[:, 0].reshape(-1, 1)
        
        # Se busca a traves de todos los segmentos
        for j, segmento_comparar in enumerate(arrays_resultantes_final):
            if i == j:
                continue
                
            # Se calculan las distancias desde el primer punto del segmento actual a todos los puntos del segmento comparado
            for k in range(segmento_comparar.shape[1]):
                punto_comparar = segmento_comparar[:, k].reshape(-1, 1)
                distancia = distancia_euclidiana_mod(primer_punto_actual, punto_comparar)
                
                # Se actualiza el punto mas cercano si se encuentra una distancia menor
                if distancia < distancia_minima:
                    distancia_minima = distancia
                    punto_mas_cercano = punto_comparar
        
        # Se agregar el punto mas cercano al inicio del segmento actual
        if punto_mas_cercano is not None and distancia_minima < 2:
            segmento_ajustado = np.hstack([punto_mas_cercano, segmento_actual])
        else:
            segmento_ajustado = segmento_actual
        
        segmentos_ajustados.append(segmento_ajustado)

    # Contenedor para los nuevos segmentos ajustados
    segmentos_procesados = []

    for segmento in segmentos_ajustados:
        # Se calcula la diferencia entre coordenadas consecutivas
        diferencias = np.diff(segmento, axis=1)
        # Se elimina la primera coordenada original dejando las diferencias
        segmento_procesado = diferencias
        segmentos_procesados.append(segmento_procesado)

    # Ruta del archivo donde se guardarán las coordenadas
    ruta_base_f = f"Objetos3D/BaseDeMalla/{ruta_rotacion}/"

    # Se asegura de que la ruta base existe, si no, se crea
    if not os.path.exists(ruta_base_f):
        os.makedirs(ruta_base_f)

    # Se genera un nombre de archivo unico para cada conjunto de resultados
    nombre_archivo_f = f"BaseDeMalla{ruta_rotacion}-{idx}.txt"
    ruta_archivo_f = os.path.join(ruta_base_f, nombre_archivo_f)

    # Se abre el archivo para escribir las coordenadas
    with open(ruta_archivo_f, "w") as archivo:
        for i, sub_array in enumerate(segmentos_procesados):
            # Se determina si se necesita añadir un parentesis extra
            parentesis_extra = "()" if i % 2 != 0 else ""
            
            # Se escribe el parentesis inicial extra si es necesario
            if parentesis_extra:
                archivo.write(parentesis_extra[0])
                
            # Se escriben las coordenadas
            coordenadas = ", ".join(f"({x},{y},{z})" for x, y, z in zip(sub_array[0], sub_array[1], sub_array[2]))
            archivo.write(coordenadas)
            
            # Se escribe el parentesis final extra si es necesario
            if parentesis_extra:
                archivo.write(parentesis_extra[1])

    return segmentos_procesados

