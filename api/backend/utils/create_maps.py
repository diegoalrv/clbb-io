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

# Importa el modelo Map
from backend.models.maps import Map
from backend.models.slots import Slot

slider = {
     'diversidad_suelo': 1,
     'educacion': 2,
     'proximidad_cultura': 3,
     'poblacion': 4,
     'parques': 6,
     'plazas': 7
}

Map.objects.all().delete()

# Ruta de la carpeta que contiene las imágenes
carpeta_imagenes = '/app/media/final_maps/'  # Ajusta la ruta según tu estructura

subcarpetas = [d for d in os.listdir(carpeta_imagenes) if os.path.isdir(os.path.join(carpeta_imagenes, d))]


for carpeta in subcarpetas: 
    # Obtén la lista de archivos en la carpeta
    subcarpeta_path = os.path.join(carpeta_imagenes, carpeta)

    # Lista todos los archivos en la subcarpeta
    archivos_en_subcarpeta = os.listdir(subcarpeta_path)

    # Filtra los archivos que siguen el patrón 0001100
    # archivos_filtrados = [archivo for archivo in archivos if archivo.isdigit() and len(archivo) == 7]

    # Ordena los archivos según su número
    archivos_ordenados = sorted(archivos_en_subcarpeta)

    nombre_mapa = carpeta.replace('mapas_', '')

    # Recorre los archivos y crea instancias de Map
    for archivo in archivos_ordenados:
        map_number = re.search(r'\d+', archivo)
        try:
            map_number = f'{map_number.group()}'
        except:
             print(f'Problemas con {archivo}')
             continue

        mapa = Map(
            name=f"{nombre_mapa}_{map_number}",
            slider=slider[nombre_mapa],
            image=None,
            slot1=Slot.objects.get(position_on_map=1, aruco_id=13 + int(map_number[0]) * 7),  # Ajusta según tus necesidades
            slot2=Slot.objects.get(position_on_map=2, aruco_id=14 + int(map_number[1]) * 7),
            slot3=Slot.objects.get(position_on_map=3, aruco_id=15 + int(map_number[2]) * 7),
            slot4=Slot.objects.get(position_on_map=4, aruco_id=16 + int(map_number[3]) * 7),
            slot5=Slot.objects.get(position_on_map=5, aruco_id=17 + int(map_number[4]) * 7),
            slot6=Slot.objects.get(position_on_map=6, aruco_id=18 + int(map_number[5]) * 7),
            slot7=Slot.objects.get(position_on_map=7, aruco_id=19 + int(map_number[6]) * 7)
        )

        # Construye la ruta completa de la imagen
        ruta_imagen = os.path.join(subcarpeta_path, archivo)

        if os.path.exists(ruta_imagen):
                with open(ruta_imagen, 'rb') as imagen_file:
                    mapa.image.save(f'{nombre_mapa}/{map_number}.png', File(imagen_file), save=True)

        mapa.save()

        print(f"Mapa creado: {mapa.name}, Imagen: {mapa.image}")

# Obtén la ruta de la primera imagen (si existe)
# primera_imagen = os.path.join('maps', archivos_ordenados[0]) if archivos_ordenados else None

# print("Ruta de la primera imagen:", primera_imagen)
