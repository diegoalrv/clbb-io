# Variables globales para la ejecución del server
# Mantiene revisado que tipo de mapa y el estado de este (placas)

map_type = None
map_state = None
aestatic_type = None
list_temp = []

SLOTS_IDS = {
    '13': 0,
    '14': 1,
    '15': 2,
    '16': 3,
    '17': 4,
    '18': 5,
    '19': 6
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