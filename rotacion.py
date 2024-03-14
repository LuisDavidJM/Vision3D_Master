import trimesh
import numpy as np
import os

######################### ROTAR LOS OBJETOS OBJ ######################################

def rotar_guardar_obj(ruta_archivo, ruta_destino, eje, grados):
    # Se carga el modelo OBJ
    mesh = trimesh.load_mesh(ruta_archivo)
    
    # Se calcula la matriz de rotación
    matriz_rot = trimesh.transformations.rotation_matrix(np.radians(grados), eje)
    
    # Se aplica la rotación
    mesh.apply_transform(matriz_rot)
    
    # Se guarda el modelo rotado
    mesh.export(ruta_destino)

def procesar_archivos(directorio_fuente, directorios_destino, grados_rotacion):
    # Se asegura de que las rutas de destino existan
    for dir in directorios_destino.values():
        os.makedirs(dir, exist_ok=True)
    
    # Se listan todos los archivos OBJ
    archivos = [f for f in os.listdir(directorio_fuente) if f.endswith('.obj')]
    
    # Se procesa cada archivo
    for archivo in archivos:
        ruta_archivo = os.path.join(directorio_fuente, archivo)
        for grados, directorio in directorios_destino.items():
            nombre_salida = f"{os.path.splitext(archivo)[0]}_{grados}grados.obj"
            ruta_destino = os.path.join(directorio, nombre_salida)
            # Se elige el eje Y para rotación
            rotar_guardar_obj(ruta_archivo, ruta_destino, [0, 1, 0], grados)  

directorio_fuente = '../Objetos3D/ArchivosOBJ/Original'
directorios_destino = {
    15: '../Objetos3D/ArchivosOBJ/Rotado15',
    25: '../Objetos3D/ArchivosOBJ/Rotado25',
    45: '../Objetos3D/ArchivosOBJ/Rotado45',
    75: '../Objetos3D/ArchivosOBJ/Rotado75'
}

# Se ejecuta el procesamiento de las rotaciones
procesar_archivos(directorio_fuente, directorios_destino, [15, 25, 45, 75])


