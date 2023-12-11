from PIL import Image
import os

def combinar_imagenes(ruta_carpeta, nombre_salida, espacio_blanco=5):
    # Lista todas las imágenes en la carpeta
    imagenes = [f for f in os.listdir(ruta_carpeta) if f.endswith('.png') or f.endswith('.jpg')]

    if not imagenes:
        print("No se encontraron imágenes en la carpeta.")
        return

    # Lee la primera imagen para obtener sus dimensiones
    primera_imagen = Image.open(os.path.join(ruta_carpeta, imagenes[0]))
    ancho, alto = primera_imagen.size

    # Calcula el número de filas y columnas
    columnas = 4
    filas = (len(imagenes) + columnas - 1) // columnas

    # Calcula las dimensiones de la imagen combinada
    ancho_combinado = (ancho + espacio_blanco) * columnas
    alto_combinado = (alto + espacio_blanco) * filas

    # Crea una imagen vacía con el tamaño total
    imagen_combinada = Image.new('RGB', (ancho_combinado, alto_combinado), color='white')

    # Combina las imágenes en la imagen combinada con espacio en blanco
    for i, imagen_nombre in enumerate(imagenes):
        columna_actual = i % columnas
        fila_actual = i // columnas

        imagen_actual = Image.open(os.path.join(ruta_carpeta, imagen_nombre))
        x = columna_actual * (ancho + espacio_blanco)
        y = fila_actual * (alto + espacio_blanco)
        imagen_combinada.paste(imagen_actual, (x, y))

    # Guarda la imagen combinada
    imagen_combinada.save(nombre_salida)
    print(f"Imagen combinada guardada como {nombre_salida}")

if __name__ == "__main__":
    ruta_carpeta = "/Users/alonsodicandia/asesorias/clbb-io/camera/images/aruco_marker/"
    nombre_salida = "/Users/alonsodicandia/asesorias/clbb-io/camera/images/all_markers/imagen_combinada.png"
    combinar_imagenes(ruta_carpeta, nombre_salida)
