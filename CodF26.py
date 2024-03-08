import Esqueletos

ruta_rotacion = ["Original", "Rotado15", "Rotado25", "Rotado45", "Rotado75"]

# Coordenadas de los 10 esqueletos originales y cada rotación
out_original = Esqueletos.manejo_de_archivos(ruta_rotacion[0])
out_15 = Esqueletos.manejo_de_archivos(ruta_rotacion[1])
out_25 = Esqueletos.manejo_de_archivos(ruta_rotacion[2])
out_45 = Esqueletos.manejo_de_archivos(ruta_rotacion[3])
out_75 = Esqueletos.manejo_de_archivos(ruta_rotacion[4])

#print(out[0])