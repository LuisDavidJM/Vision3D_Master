from Diccionarios import diccionario_3drc
from Coordenadas import ajuste_coordenadas
import numpy as np
import Esqueletos
import matplotlib.pyplot as plt

# Función para calcular el angulo entre dos puntos
def calcular_angulo(punto_a, punto_c):
    vector_a = np.array(punto_a)
    vector_c = np.array(punto_c)
    producto_punto = np.dot(vector_a, vector_c)
    norma_a = np.linalg.norm(vector_a)
    norma_c = np.linalg.norm(vector_c)
    coseno_angulo = producto_punto / (norma_a * norma_c)
    angulo_radianes = np.arccos(np.clip(coseno_angulo, -1.0, 1.0))
    angulo_grados = np.degrees(angulo_radianes)
    return angulo_grados

# Función para calcular la distancia entre dos puntos
def calcular_distancia(punto_b, punto_c):
    return np.linalg.norm(-np.array(punto_b) - np.array(punto_c))

# Función para comparar los datos calculados con el diccionario y generar letras
def comparar_y_generar_letras(puntos):
    puntos = puntos.T
    letras = []
    # Ciclo para generar los valores de las coordenadas
    for i in range(0, len(puntos) - 2, 1):
        angulo = round(calcular_angulo(puntos[i], puntos[i+2]))
        distancia = round(calcular_distancia(puntos[i+1], puntos[i+2]), 4)
        producto_cruz = tuple(np.cross(puntos[i], puntos[i+2]))
        
        # Se buscan las coincidencias en el diccionario
        clave = (angulo, distancia, producto_cruz)
        if clave in diccionario_3drc:
            letras.append(diccionario_3drc[clave])
        else:
            encontrado = False
            for clave in diccionario_3drc.keys():
                angulo_dic, distancia_dic, _ = clave 
                if angulo == angulo_dic and distancia == distancia_dic:
                    letras.append(diccionario_3drc[clave])
                    encontrado = True
                    break
            if not encontrado:    
                letras.append("y")

    return letras

def cadenas_y_frecuencia(coordenadas, ruta_rotacion, idx):
    coord = ajuste_coordenadas(coordenadas, ruta_rotacion, idx)

    ######################### CADENA RESULTANTE #################################

    resultado_final = ""

    # Ciclo para recorrer todos los objetos y obtener sus cadenas
    for i, seg in enumerate(coord, start=1):
        letras_encontradas = comparar_y_generar_letras(seg)
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

######################### CODIGO PRINCIPAL #################################

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


ruta_rotacion = ["Original", "Rotado15", "Rotado25", "Rotado45", "Rotado75"]
angulos = [0, 15, 25, 45, 75]
frecuencias_globales_por_objeto = {i: {} for i in range(10)}

for i in range(10):
    frecuencias_agregadas = {symbol: [] for symbol in diccionario_3drc.values()}
    print(f"\n------------------------- OBJETO {i} -------------------------")
    for angulo, ruta in zip(angulos, ruta_rotacion):
        #print(ruta)
        out = Esqueletos.manejo_de_archivos(ruta)
        print(f"\nCODIFICACIÓN 3DRC PARA ROTACIÓN {angulo} GRADOS:")
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
