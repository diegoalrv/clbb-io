# init_coin_script.py

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
from backend.models.coins import Coin

# Lista de áreas y números asociados
areas = {
    'AREAS VERDES': 3,
    'CICLOVIA ACTUAL': 4,
    'CICLOVIA FUTURA': 5,
    'PROPUESTA CICLOVIA': 6,
    'CALIDAD ACERAS': 7,
    'MODELO AGENTES': 8,
    'PUENTE': 9,
}

# Función para inicializar objetos Coin
def init_coins():
    # Verifica si ya existen objetos Coin en la base de datos
    if Coin.objects.exists():
        print("Ya existen objetos Coin. No se realizará ninguna acción.")
        return

    # Crea los objetos Coin según la lista proporcionada
    for name, number in areas.items():
        Coin.objects.create(
            name=name,
            aruco_id=number,
            aruco_marker=None  # Puedes ajustar esto según tus necesidades
        )
        print(f"Coin creado: {name}")

# Ejecuta la función de inicialización
if __name__ == "__main__":
    init_coins()
    print("Inicialización completa.")
