# Variables globales para la ejecución del server
# Mantiene revisado que tipo de mapa y el estado de este (placas)

INDICATOR_ID = 1
INDICATOR_STATE = {
    0: 0,
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
}
buffer_interface = []

SLOTS_IDS = {
    '13': (0, 0),
    '14': (1, 0),
    '15': (2, 0),
    '16': (3, 0),
    '17': (4, 0),
    '18': (5, 0),
    '19': (6, 0),
    '20': (0, 1),
    '21': (1, 1),
    '22': (2, 1),
    '23': (3, 1),
    '24': (4, 1),
    '25': (5, 1),
    '26': (6, 1),
}

"""
map_type value of each indicator map

 OK 1) Diversidad de Suelo
 OK 2) Educación
 OK 3) Proximidad de cultura
 OK 4) Población
 5) Entretenimiento
 OK 6) Parques
 OK 7) Plazas
 8) Aprovisionamiento
 9) Comercio
 10) Edificacion
 10+1) Salud
"""