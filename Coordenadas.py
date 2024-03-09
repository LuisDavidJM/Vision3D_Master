import numpy as np

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


def ajuste_coordenadas(out):
    ######################### AJUSTAR COORDENADAS ###################################################

    out_inicio = out - out[:, 0][:, np.newaxis]

    ######################### IDENTIFICAR LAS RAMAS ###################################################

    # Calcular las diferencias entre puntos adyacentes
    diferencias = np.diff(out_inicio, axis=1)

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
            segmento = out_inicio[:, inicio:i]
            arrays_resultantes.append(segmento)
            inicio = i  # Actualizar el índice de inicio para el próximo segmento

    # No olvidar agregar el último segmento después del último salto encontrado
    if inicio < out_inicio.shape[1]:
        segmento_final = out_inicio[:, inicio:]
        arrays_resultantes.append(segmento_final)

    # Separar los segmentos en dos listas basadas en su longitud
    segmentos_largos = [seg for seg in arrays_resultantes if seg.shape[1] > 15]
    segmentos_cortos = [seg for seg in arrays_resultantes if seg.shape[1] <= 15]

    # Combinar las listas, poniendo los segmentos cortos al final
    arrays_resultantes_ordenados = segmentos_largos + segmentos_cortos

    ######################### ACOMODAR LAS RAMAS ###################################################

    # Iterar sobre los arrays resultantes, modificando los necesarios
    for i in range(1, len(segmentos_largos)):  # Empezar desde el segundo
        primer_punto = segmentos_largos[i][:, 0]  # Primera coordenada del array actual
        # Todos los otros arrays, excepto el actual
        otros_arrays = segmentos_largos[:i] + segmentos_largos[i+1:]
        
        # Aplanar la lista de otros arrays para facilitar la comparación
        otros_arrays_aplanados = np.hstack(otros_arrays)
        
        # Verificar si existe alguna distancia menor a 2
        if not existe_distancia_menor_a_2(primer_punto, otros_arrays):
            # Invertir el array actual si no hay distancias menores a 2
            segmentos_largos[i] = np.flip(segmentos_largos[i], axis=1)

    # Combinar nuevamente los arrays, manteniendo los cortos al final
    arrays_resultantes_final = segmentos_largos + segmentos_cortos

    ######################### AJUSTES PARA CODIFICAR ###################################################

    # Preparar un nuevo contenedor para los segmentos ajustados
    segmentos_ajustados = [arrays_resultantes_final[0]]  # El primer segmento permanece igual

    # Procesar cada segmento a partir del segundo
    for i in range(1, len(arrays_resultantes_final)):
        segmento_actual = arrays_resultantes_final[i]
        punto_mas_cercano = None
        distancia_minima = np.inf
        
        # Primer punto del segmento actual
        primer_punto_actual = segmento_actual[:, 0].reshape(-1, 1)
        
        # Buscar a través de todos los segmentos, incluido el propio segmento
        for j, segmento_comparar in enumerate(arrays_resultantes_final):
            if i == j:
                continue  # No comparar el segmento consigo mismo
                
            # Calcular distancias desde el primer punto del segmento actual a todos los puntos del segmento a comparar
            for k in range(segmento_comparar.shape[1]):
                punto_comparar = segmento_comparar[:, k].reshape(-1, 1)
                distancia = distancia_euclidiana_mod(primer_punto_actual, punto_comparar)
                
                # Actualizar el punto más cercano si se encuentra una distancia menor
                if distancia < distancia_minima:
                    distancia_minima = distancia
                    punto_mas_cercano = punto_comparar
        
        # Agregar el punto más cercano al inicio del segmento actual, si se encontró alguno
        if punto_mas_cercano is not None and distancia_minima < 2:
            segmento_ajustado = np.hstack([punto_mas_cercano, segmento_actual])
        else:
            segmento_ajustado = segmento_actual
        
        segmentos_ajustados.append(segmento_ajustado)

    return segmentos_ajustados

