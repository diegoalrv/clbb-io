# init_script.py

import os, sys, re
import io
from PIL import Image
from django.core.files.images import ImageFile
from django.core.files import File
from django.core.wsgi import get_wsgi_application
from django.db import models

# Configura la aplicación Django
current_path = os.path.abspath(os.path.dirname(__file__))
current_path = current_path[:current_path.find(os.path.dirname(__file__))]
sys.path.append(current_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clbb.settings')
application = get_wsgi_application()

# Importa el modelo static
from backend.models.aestatics import AeStatic
#from backend.models.slots import Slot

# Ruta de la carpeta que contiene las imágenes
carpeta_imagenes = '/app/media/image_static/'  # Ajusta la ruta según tu estructura

subcarpetas = [d for d in os.listdir(carpeta_imagenes) if os.path.isdir(os.path.join(carpeta_imagenes, d))]

#print(subcarpetas)

for carpeta in subcarpetas: 
    # Obtén la lista de archivos en la carpeta
    subcarpeta_path = os.path.join(carpeta_imagenes, carpeta)

    # Lista todos los archivos en la subcarpeta
    archivos_en_subcarpeta = os.listdir(subcarpeta_path)

    # Filtra los archivos que siguen el patrón 0001100
    # archivos_filtrados = [archivo for archivo in archivos if archivo.isdigit() and len(archivo) == 7]

    # Ordena los archivos según su número
    archivos_ordenados = sorted(archivos_en_subcarpeta)

    # nombre_static = carpeta.replace('aestatic_', '')
    print(len(archivos_en_subcarpeta))
    slider = {}
    contador = 100


    # Recorre los archivos y crea instancias de Map
    for archivo in archivos_ordenados:
        # print(archivo)
        gif = AeStatic(
            name=f"{archivo.replace('.gif', '')}",
            slider= contador,
            aestatic_file=None,
        )

        # # Construye la ruta completa de la imagen
        ruta_imagen = os.path.join(subcarpeta_path, archivo)

        if os.path.exists(ruta_imagen):
            with open(ruta_imagen, 'rb') as imagen_file:
                gif.aestatic_file.save(f'{archivo}.gif', File(imagen_file), save=True)

        gif.save()
        contador += 1
        print(f"Mapa creado: {gif.name}, Imagen: {gif.aestatic_file}")