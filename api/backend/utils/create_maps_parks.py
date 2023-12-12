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

Map.objects.all().delete()
# Ruta de la carpeta que contiene las imágenes
carpeta_imagenes = '/app/media/mapas_maqueta_prueba1/'  # Ajusta la ruta según tu estructura

# Obtén la lista de archivos en la carpeta
archivos = os.listdir(carpeta_imagenes)

# Filtra los archivos que siguen el patrón 0001100
# archivos_filtrados = [archivo for archivo in archivos if archivo.isdigit() and len(archivo) == 7]

# Ordena los archivos según su número
archivos_ordenados = sorted(archivos)

# Recorre los archivos y crea instancias de Map
for archivo in archivos_ordenados:
    map_number = re.search(r'\d+', archivo)
    map_number = f'm{map_number.group()}'

    mapa = Map(
        name=f"Map_proximity_to_parks_{map_number}",
        slider=6,
        coin=None,
        image=None,
        slot1=Slot.objects.get(position_on_map=1, aruco_id=13 + int(map_number[1]) * 7),  # Ajusta según tus necesidades
        slot2=Slot.objects.get(position_on_map=2, aruco_id=14 + int(map_number[2]) * 7),
        slot3=Slot.objects.get(position_on_map=3, aruco_id=15 + int(map_number[3]) * 7),
        slot4=Slot.objects.get(position_on_map=4, aruco_id=16 + int(map_number[4]) * 7),
        slot5=Slot.objects.get(position_on_map=5, aruco_id=17 + int(map_number[5]) * 7),
        slot6=Slot.objects.get(position_on_map=6, aruco_id=18 + int(map_number[6]) * 7),
        slot7=Slot.objects.get(position_on_map=7, aruco_id=19 + int(map_number[7]) * 7)
    )
    # Construye la ruta completa de la imagen
    ruta_imagen = os.path.join(carpeta_imagenes, archivo)

    # Abre la imagen con Pillow y asígnala al campo ImageField
    # if os.path.exists(ruta_imagen):
    #     imagen = Image.open(ruta_imagen)
    #     imagen_bytes = imagen.tobytes()
    #     image_file = ImageFile(io.BytesIO(imagen_bytes), name=f'Proximity_to_parks_{map_number}.png')
    #     mapa.image = image_file
    if os.path.exists(ruta_imagen):
            with open(ruta_imagen, 'rb') as imagen_file:
                mapa.image.save(f'Proximity_to_parks_{map_number}.png', File(imagen_file), save=True)

    mapa.save()

    print(f"Mapa creado: {mapa.name}, Imagen: {mapa.image}")

# Obtén la ruta de la primera imagen (si existe)
# primera_imagen = os.path.join('maps', archivos_ordenados[0]) if archivos_ordenados else None

# print("Ruta de la primera imagen:", primera_imagen)
