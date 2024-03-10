#from Diccionarios import diccionario_3drc
from Coordenadas import ajuste_coordenadas
import numpy as np
import Esqueletos
import sys

######################### CODIGO PRINCIPAL #################################

ruta_rotacion = ["Original", "Rotado15", "Rotado25", "Rotado45", "Rotado75"]

#print("OPCIONES: 0, 15, 25, 45, 75")
#grados = input("Selecciona un grado: ")
grados = "0"

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




coord = ajuste_coordenadas(out[0], ruta_rotacion, 0)

# Mostrar los segmentos
for i, seg in enumerate(coord, start=1):
    print(f"Segmento {i}:")
    print(seg)
    print()
