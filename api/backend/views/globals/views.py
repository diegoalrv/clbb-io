from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
import requests
from backend import globals
from backend.models.maps import Map
from django.db.models import Q

@csrf_exempt
def set_map_type(request):
    print(request.body)
    if request.method == 'POST':        
        data = json.loads(request.body)
        print(data)
        globals.map_type = data.get('map_type')
        return check_and_send_map()
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def set_map_state(request):
    if request.method == 'GET':
        slots_param = request.GET.get('slots', '')  # Obtiene el parámetro 'slots' de la URL
        if slots_param:
            slots_list = sorted(slots_param.split(','))
            for num in slots_list:
                if int(num) >= 20:
                    slots_list.remove(num)
                    slots_list.insert(globals.SLOTS_IDS[str(int(num)-7)], num)
            globals.map_state = slots_list  # Actualiza la variable global
            return check_and_send_map()
        else:
            return JsonResponse({'error': 'No slots parameter provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

def get_filter_map():
    # Utiliza las variables globales para filtrar el queryset
    slider_param = globals.map_type
    slots_list = globals.map_state

    queryset = Map.objects.all()

    queryset = queryset.filter(
        Q(slider=slider_param) &
        Q(slot1__aruco_id=slots_list[0]) &
        Q(slot2__aruco_id=slots_list[1]) &
        Q(slot3__aruco_id=slots_list[2]) &
        Q(slot4__aruco_id=slots_list[3]) &
        Q(slot5__aruco_id=slots_list[4]) &
        Q(slot6__aruco_id=slots_list[5]) &
        Q(slot7__aruco_id=slots_list[6])
    )

    # Obtén el mapa correspondiente (asumiendo que quieres el primero que coincida)
    map_instance = queryset.first()
    return map_instance if map_instance else None

def check_and_send_map():
    if globals.map_type and globals.map_state:
        # Aquí implementas la lógica para obtener la URL del mapa
        map_instance = get_filter_map()
        if map_instance:
            # Enviar la URL a otro servicio
            send_map_url_to_service(map_instance.image)
            return JsonResponse({'message': 'Map processed and sent'})
    return JsonResponse({'message': 'Map type or state not set'})

def send_map_url_to_service(map_url):
    # Implementa la lógica para enviar la URL a otro servicio
    print(map_url.name)
    #return JsonResponse({'message': map_url.name})
    # base_url = 'http://localhost:5000'
    base_url = 'http://bug-free-train-backend-1:5000'
    endpoint = 'post-image'
    response = requests.post(f'{base_url}/{endpoint}', json={'url': map_url.name})
    print(response.status_code)

def get_global_variables(request):
    data = {
        'map_type': globals.map_type,
        'map_state': globals.map_state
    }
    return JsonResponse(data)

