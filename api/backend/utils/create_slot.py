# init_script.py

import os, sys
from django.core.wsgi import get_wsgi_application
from django.db import models

# Configura la aplicación Django
current_path = os.path.abspath(os.path.dirname(__file__))
current_path = current_path[:current_path.find(os.path.dirname(__file__))]
sys.path.append(current_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clbb.settings')
application = get_wsgi_application()

# Importa los modelos necesarios
from backend.models.slots import Slot

# Función para inicializar objetos Slot
def init_slots():
    state = ['Presente', 'Futuro']
    # Verifica si ya existen objetos Slot en la base de datos
    if Slot.objects.exists():
        print("Ya existen objetos Slot. No se realizará ninguna acción.")
        return

    first_aruco = 12
    for slot_state in state:
        # Crea los objetos Slot según el patrón
        for i in range(1, 8):
            slot_name = f"{slot_state}_{i}"
            aruco_id = first_aruco + i  # Comienza en 13 y se incrementa en 1
            aruco_marker = f'/Users/alonsodicandia/asesorias/clbb-io/camera/images/aruco_marker/marker_{aruco_id}.png'  # Ajusta la extensión de la imagen según tu caso
            position_on_map = i
            lego_image = None

            Slot.objects.create(
                name=slot_name,
                aruco_id=aruco_id,
                aruco_marker=aruco_marker,
                position_on_map=position_on_map,
                lego_image=lego_image
            )
            print(f"Slot creado: {slot_name}")
        
        first_aruco += 7

# Ejecuta la función de inicialización
if __name__ == "__main__":
    init_slots()
    print("Inicialización completa.")
