# Variables globales para la ejecución del server
# Mantiene revisado que tipo de mapa y el estado de este (placas)

INDICATOR_ID = 1
INDICATOR_STATE = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
}
buffer_interface = []

SLOTS_IDS = {
    '13': (1, 0),
    '14': (2, 0),
    '15': (3, 0),
    '16': (4, 0),
    '17': (5, 0),
    '18': (6, 0),
    '19': (7, 0),
    '20': (1, 1),
    '21': (2, 1),
    '22': (3, 1),
    '23': (4, 1),
    '24': (5, 1),
    '25': (6, 1),
    '26': (7, 1),
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