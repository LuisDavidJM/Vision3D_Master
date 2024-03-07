import numpy as np
from skimage.measure import marching_cubes
import ezdxf

# Ruta al archivo NumPy binario que contiene tu esqueleto
nombre_archivo_numpy = '../Objetos3D/Pruebas/esqueleto_podado.npy'
esqueleto = np.load(nombre_archivo_numpy)

# Aplica Marching Cubes al esqueleto para obtener la malla
# Ajusta el nivel si es necesario para tu conjunto de datos específico
vertices, caras, _, _ = marching_cubes(esqueleto, level=0.5)

# vertices: Array de las posiciones de los vértices en el espacio 3D
# caras: Array de índices de vértices que forman cada triángulo de la malla

def exportar_a_dxf(vertices, caras, nombre_archivo_salida):
    # Crear un nuevo dibujo DXF
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # Añadir una MESH al espacio modelo
    mesh = msp.add_mesh()
    
    # Preparar la malla para la adición de vértices y caras
    with mesh.edit_data() as mesh_data:
        # Añadir vértices a la malla
        mesh_data.vertices = vertices
        
        # Añadir caras a la malla
        # Las caras en ezdxf se definen por índices a los vértices, que es lo que proporciona `caras`
        mesh_data.faces = caras
    
    # Guardar el archivo DXF
    doc.saveas(nombre_archivo_salida)

# Uso de la función
nombre_archivo_salida = '../Objetos3D/Pruebas/esqueleto_podado.dxf'
exportar_a_dxf(vertices, caras, nombre_archivo_salida)
