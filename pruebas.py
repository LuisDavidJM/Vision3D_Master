# Norma (Longitud)
import numpy as np

# Lista de puntos, donde cada punto es una tupla (x, y, z)
puntos = [(1, 0, 0), (0, 0, 1), (1, 0, 1)]

# Calculando la norma para cada punto
for punto in puntos:
    norma = np.linalg.norm(np.array(punto))
    #print(f"La norma del punto {punto} es {norma}")





# Definiendo los puntos
punto1 = np.array([0, 0, 1])
punto3 = np.array([-1, 0, 1])

# Calculando los vectores desde el origen hasta cada punto
vector1 = punto1
vector3 = punto3

# Calculando el producto punto entre los dos vectores
producto_punto = np.dot(vector1, vector3)

# Calculando las normas de los vectores
norma_vector1 = np.linalg.norm(vector1)
norma_vector3 = np.linalg.norm(vector3)

# Calculando el ángulo en radianes
angulo_radianes = np.arccos(producto_punto / (norma_vector1 * norma_vector3))

# Convirtiendo el ángulo a grados
angulo_grados = int(np.degrees(angulo_radianes))

#print(f"El ángulo entre el punto 1 ({punto1}) y el punto 3 ({punto3}) es de {angulo_grados} grados")




# Array principal que contiene tres arrays: x, y, z
# Por ejemplo:
array_principal = np.array([
    [0, 0, 1],  # x
    [0, 0, 0], # y
    [1, 1, 0] # z
])

# Transponiendo el array principal para obtener un array de puntos (n, 3)
puntos = array_principal.T

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

# Calculando y mostrando los ángulos, distancias y producto cruz
for i in range(0, len(puntos) - 2, 1):  # Iterar hasta el antepenúltimo punto
    angulo = round(calcular_angulo(puntos[i], puntos[i+2]))
    distancia = round(calcular_distancia(puntos[i+1], puntos[i+2]), 4)
    producto_cruz = np.cross(puntos[i], puntos[i+2])
    print(f"Entre el punto {i+1} y el punto {i+3}:")
    print(f"  Ángulo: {angulo} grados")
    print(f"  Distancia: {distancia}")
    print(f"  Producto cruz: {producto_cruz}")