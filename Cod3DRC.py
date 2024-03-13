from Diccionarios import diccionario_3drc
from Coordenadas import ajuste_coordenadas
import numpy as np
import Esqueletos
import sys

# Función para calcular el ángulo entre dos puntos
def calcular_angulo(punto_a, punto_c):
    vector_a = np.array(punto_a)
    vector_c = np.array(punto_c)
    producto_punto = np.dot(vector_a, vector_c)
    norma_a = np.linalg.norm(vector_a)
    norma_c = np.linalg.norm(vector_c)
    coseno_angulo = producto_punto / (norma_a * norma_c)
    angulo_radianes = np.arccos(np.clip(coseno_angulo, -1.0, 1.0))  # Asegurar que el valor esté en el rango válido para arccos
    angulo_grados = np.degrees(angulo_radianes)
    return angulo_grados

# Función para calcular la distancia entre dos puntos
def calcular_distancia(punto_b, punto_c):
    return np.linalg.norm(-np.array(punto_b) - np.array(punto_c))

# Función para comparar los datos calculados con el diccionario y generar letras
def comparar_y_generar_letras(puntos):
    # Intercambiar los ejes x, z
    #puntos[[0, 2]] = puntos[[2, 0]]
    puntos = puntos.T
    #print(puntos)
    letras = []
    for i in range(0, len(puntos) - 2, 1):  # Asumiendo puntos es una lista de 3 listas (x, y, z)
        angulo = round(calcular_angulo(puntos[i], puntos[i+2]))
        distancia = round(calcular_distancia(puntos[i+1], puntos[i+2]), 4)
        producto_cruz = tuple(np.cross(puntos[i], puntos[i+2]))
        
        # Buscar coincidencias en el diccionario
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

    for i, seg in enumerate(coord, start=1):
        # Transponiendo el array principal para obtener un array de puntos (n, 3)
        letras_encontradas = comparar_y_generar_letras(seg)
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
print("#################### CODIFICACIÓN 3DRC ####################")
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