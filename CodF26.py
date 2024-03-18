from Diccionarios import diccionario_f26
from Coordenadas import ajuste_coordenadas
import numpy as np
import Esqueletos
import matplotlib.pyplot as plt

# Función para comparar las coordenadas con el diccionario
def buscar_letras(coordenadas_array):
    letras = []
    # Se obtienen las coordenadas en tuplas (x, y, z)
    coordenadas_transpuestas = np.transpose(coordenadas_array)

    for coordenada in coordenadas_transpuestas:
        # Se convierte la tupla de numpy a una tupla de Python para que coincida con el diccionario
        coordenada_tupla = tuple(coordenada)
        if coordenada_tupla in diccionario_f26:
            letras.append(diccionario_f26[coordenada_tupla])
        else:
            letras.append('')
    return letras


def cadenas_y_frecuencia(coordenadas, ruta_rotacion, idx):
    coord = ajuste_coordenadas(coordenadas, ruta_rotacion, idx)

    ######################### CADENA RESULTANTE #################################

    resultado_final = ""

    # Ciclo para recorrer todos los objetos y obtener sus cadenas
    for i, seg in enumerate(coord, start=1):
        letras_encontradas = buscar_letras(seg)
        if i % 2 == 0:
            segmento_en_letras = "(" + "".join(letras_encontradas) + ")"
        else:
            segmento_en_letras = "".join(letras_encontradas)
        resultado_final += segmento_en_letras

    ######################### FRECUENCIA DE APARICION #################################

    resultado_sin_parentesis = resultado_final.replace("(", "").replace(")", "")

    # Se calcula la frecuencia de aparición de cada símbolo
    frecuencias = {}
    for simbolo in resultado_sin_parentesis:
        if simbolo not in frecuencias:
            frecuencias[simbolo] = 1
        else:
            frecuencias[simbolo] += 1

    # Se ordena el diccionario de frecuencias alfabéticamente
    frecuencias_ordenadas = dict(sorted(frecuencias.items()))

    return resultado_final, frecuencias_ordenadas

# Función para imprimir la frecuencia de los simbolos
def imprimir_tabla(frecuencias):
    print("Símbolo\tFrecuencia")
    for simbolo, frecuencia in frecuencias.items():
        frecuencia = frecuencias.get(simbolo, 0)
        print(f"{simbolo}\t{frecuencia}")


def imprimir_y_graficar_frecuencias(frecuencias, titulo):
    simbolos = list(frecuencias.keys())
    counts = list(frecuencias.values())
    plt.figure(figsize=(10, 6))
    plt.bar(simbolos, counts)
    plt.title(titulo)
    plt.xlabel('Símbolos')
    plt.ylabel('Frecuencia')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

######################### CODIGO PRINCIPAL #################################

ruta_rotacion = ["Original", "Rotado15", "Rotado25", "Rotado45", "Rotado75"]
angulos = [0, 15, 25, 45, 75]
frecuencias_globales_por_objeto = {i: {} for i in range(10)} 

for i in range(10):
    frecuencias_agregadas = {symbol: [] for symbol in diccionario_f26.values()}
    print(f"\n------------------------- OBJETO {i} -------------------------")
    for angulo, ruta in zip(angulos, ruta_rotacion):
        #print(ruta)
        out = Esqueletos.manejo_de_archivos(ruta)
        print(f"\nCODIFICACIÓN F26 PARA ROTACIÓN {angulo} GRADOS:")
        cadena_producida, frecuencias = cadenas_y_frecuencia(out[i], ruta, i)
        print("\nCadena producida:")
        print(cadena_producida)
        print("\nFrecuencia de aparición:")
        imprimir_tabla(frecuencias)
        for simbolo, frecuencia in frecuencias.items():
            frecuencias_agregadas[simbolo].append(frecuencia)

    # Se calcula el promedio de frecuencias después de todas las rotaciones para este objeto
    promedios_frecuencias = {simbolo: sum(vals) / len(vals) if len(vals) > 0 else 0 for simbolo, vals in
                             frecuencias_agregadas.items()}

    frecuencias_globales_por_objeto[i] = promedios_frecuencias
    print("\nPromedio de frecuencias:")
    imprimir_tabla(promedios_frecuencias)
    imprimir_y_graficar_frecuencias(promedios_frecuencias, f'Promedio de Frecuencias para Objeto {i}')
