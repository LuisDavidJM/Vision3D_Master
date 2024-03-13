from Diccionarios import diccionario_f26
from Coordenadas import ajuste_coordenadas
import numpy as np
import Esqueletos
import sys

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
            letras.append('')
    return letras

def cadenas_y_frecuencia(coordenadas, ruta_rotacion, idx):
    coord = ajuste_coordenadas(coordenadas, ruta_rotacion, idx)

    ######################### CADENA RESULTANTE #################################

    resultado_final = ""

    for i, seg in enumerate(coord, start=1):
        letras_encontradas = buscar_letras(seg)
        # Si el índice es impar, no añadir paréntesis; si es par, sí añadirlos.
        if i % 2 == 0:
            # Índices pares: añadir paréntesis
            segmento_en_letras = "(" + "".join(letras_encontradas) + ")"
        else:
            # Índices impares: no añadir paréntesis
            segmento_en_letras = "".join(letras_encontradas)
        
        resultado_final += segmento_en_letras

    print("Cadena producida: ")
    print(resultado_final)

    ######################### FRECUENCIA DE APARICION #################################

    # Remover los paréntesis de la cadena
    resultado_sin_parentesis = resultado_final.replace("(", "").replace(")", "")

    # Calcular la frecuencia de aparición de cada símbolo, ignorando los paréntesis
    frecuencias = {}
    for simbolo in resultado_sin_parentesis:
        if simbolo not in frecuencias:
            frecuencias[simbolo] = 1
        else:
            frecuencias[simbolo] += 1

    # Ordenar el diccionario de frecuencias por clave (símbolo) alfabéticamente
    frecuencias_ordenadas = dict(sorted(frecuencias.items()))

    print("\nFrecuancia de aparición: ")

    # Imprimir cada frecuencia consecutivamente
    for simbolo, frecuencia in frecuencias_ordenadas.items():
        print(f"{simbolo}: {frecuencia}", end=", ")

    return frecuencias

######################### CODIGO PRINCIPAL #################################

ruta_rotacion = ["Original", "Rotado15", "Rotado25", "Rotado45", "Rotado75"]
print("#################### CODIFICACIÓN F26 ####################")
print("OPCIONES: 0, 15, 25, 45, 75")
grados = input("Selecciona un grado: ")

# Coordenadas de los 10 esqueletos originales y cada rotación
if (grados == "0"):
    out = Esqueletos.manejo_de_archivos(ruta_rotacion[0])
    ruta_rotacion = ruta_rotacion[0]
elif (grados == "15"):
    out = Esqueletos.manejo_de_archivos(ruta_rotacion[1])
    ruta_rotacion = ruta_rotacion[1]
elif (grados == "25"):
    out = Esqueletos.manejo_de_archivos(ruta_rotacion[2])
    ruta_rotacion = ruta_rotacion[2]
elif (grados == "45"):
    out = Esqueletos.manejo_de_archivos(ruta_rotacion[3])
    ruta_rotacion = ruta_rotacion[3]
elif (grados == "75"):
    out = Esqueletos.manejo_de_archivos(ruta_rotacion[4])
    ruta_rotacion = ruta_rotacion[4]
else:
    print("El valor ingresado no es valido.....")
    input("Presione ENTER para salir")
    sys.exit()

# Diccionario global para acumular frecuencias de todos los arrays
frecuencias_globales = {}

for i in range(len(out)):
    print("")
    print(f"------------------------- OBJETO {i} -------------------------")
    frecuencias = cadenas_y_frecuencia(out[i], ruta_rotacion, i)
    for simbolo, frecuencia in frecuencias.items():
        if simbolo not in frecuencias_globales:
            frecuencias_globales[simbolo] = frecuencia
        else:
            frecuencias_globales[simbolo] += frecuencia

# Calcular el promedio de la frecuencia para cada símbolo
promedios = {simbolo: frecuencia / len(out) for simbolo, frecuencia in frecuencias_globales.items()}

print("\n\n----------- PROMEDIO DE LA FRECUENCIA DE APARICION ---------")

# Imprimir los promedios de frecuencia
for simbolo, promedio in sorted(promedios.items()):
    print(f"{simbolo}: {promedio}", end=", ")

