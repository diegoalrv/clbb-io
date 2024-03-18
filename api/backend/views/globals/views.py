from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
import requests
from backend import globals
from backend.models.maps import Map
from backend.models.aestatics import AeStatic
from django.db.models import Q
import os
from django.core.serializers import serialize
import time


@csrf_exempt
def set_map_type(request):
    print(request.body)
    if request.method == 'POST':        
        data = json.loads(request.body)
        # print(data).
        globals.map_type = data.get('map_type')
        return check_and_send_map()
    elif request.method == 'GET':
        type_param = request.GET.get('map_type', 1)
        globals.map_type = type_param
        return check_and_send_map()
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def set_map_state(request):
    if request.method == 'GET':
        slots_param = request.GET.get('slots', '')  # Obtiene el parámetro 'slots' de la URL
        if slots_param:
            print('list_temp ',globals.list_temp)
            slots_list = sorted(slots_param.split(','))
            #agregar los valores a la lista vacia
            for numero in slots_list:
                if numero not in globals.list_temp:
                    globals.list_temp.append(numero) 
                    print(globals.list_temp.sort())
            # si estan los 7 valores que siga normal
            if len(globals.list_temp) == 7: 
                slots_list = globals.list_temp.copy()
                print('globals.list_temp: ',globals.list_temp)
                print('slots_list: ',slots_list)
                for num in slots_list:
                    if int(num) >= 20:
                        slots_list.remove(num)
                        slots_list.insert(globals.SLOTS_IDS[str(int(num)-7)], num)
                globals.map_state = slots_list  # Actualiza la variable global
                globals.list_temp = []
                return check_and_send_map()
            elif len(globals.list_temp) > 7:
                globals.list_temp = []
            else: 
                return JsonResponse({"error":"hay menos de 7 slots, enviar el que falta"})
        else:
            return JsonResponse({'error': 'No slots parameter provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request'},status=400)

# @csrf_exempt
# def set_map_state2(request):
#     if request.method == 'GET':
#         slots_param = request.GET.get('slots', '')  # Obtiene el parámetro 'slots' de la URL
#         if slots_param:
#             slots_list = sorted(slots_param.split(','))
#             for num in slots_list:
#                 if int(num) >= 20:
#                     slots_list.remove(num)
#                     slots_list.insert(globals.SLOTS_IDS[str(int(num)-7)], num)
#             globals.map_state = slots_list  # Actualiza la variable global
#             return check_and_send_map()
#         else:
#             return JsonResponse({'error': 'No slots parameter provided'}, status=400)
#     else:
#         return JsonResponse({'error': 'Invalid request'}, status=400)


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
    print('Check and send map')
    print(globals.map_state)
    print(globals.map_type)
    print('Condicion')
    print(globals.map_type and len(globals.map_state)>0)
    if globals.map_type and globals.map_state:
        # Aquí implementas la lógica para obtener la URL del mapa
        map_instance = get_filter_map()
        print(map_instance)
        if map_instance:
            # Enviar la URL a otro servicio
            send_map_url_to_service(map_instance.image)
            send_json_data_to_dashboard(map_instance.image)
            return JsonResponse({'message': 'Map processed and sent'})
    return JsonResponse({'message': 'Map type or state not set'})

def send_map_url_to_service(map_url):
    # Implementa la lógica para enviar la URL a otro servicio
    print(map_url.name)
    base_url = 'http://bug-free-train-backend-1:5000'
    endpoint = 'post-image'
    response = requests.post(f'{base_url}/{endpoint}', json={'url': map_url.name})
    print(response.status_code)

def send_json_data_to_dashboard(map_url):
    slot_combination = os.path.split(map_url.name)[-1].split('.')[0]
    json_path = f'media/json/{slot_combination}.json'
    with open(json_path, 'r') as json_file:
        json_data = json_file.read()
    base_url = 'http://clbb-front-backend-1:8900'
    endpoint = 'receive_data'
    response = requests.post(f'{base_url}/{endpoint}', data=json_data)

@csrf_exempt
def get_global_variables(request):
    data = {
        'map_type': globals.map_type,
        'map_state': globals.map_state
    }
    return JsonResponse(data)

# listar json de cuales son los mapas que hay
@csrf_exempt
def what_map(request):
    datos = Map.objects.all()
    sliders_unicos = set()
    data_json = []
    for x in datos:
        slider = x.slider
        name = x.name
        if slider not in sliders_unicos:
            data_json.append({'name': name, 'slider': slider})
            sliders_unicos.add(slider)
    return JsonResponse(data_json, safe=False)

# lista un json de los objetos staticos
@csrf_exempt
def what_aestatic(request):
    datos = AeStatic.objects.all()
    sliders_unicos = set()
    data_json = []
    for x in datos:
        slider = x.slider
        name = x.name
        if slider not in sliders_unicos:
            data_json.append({'name': name, 'slider': slider})
            sliders_unicos.add(slider)
    return JsonResponse(data_json, safe=False)

#  es como el set_map_type
@csrf_exempt
def loadaestetic(request):
    print(request)
    if request.method == 'GET':
        type_param = request.GET.get('loadaestetic', 1)
        print(type_param)
        skeree = request.GET.get('aestatic_type')
        print(skeree)
        globals.aestatic_type = type_param
        return check_and_send_aestetic(skeree)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def check_and_send_aestetic(valor):
    if globals.aestatic_type:
        # Aquí implementas la lógica para obtener la URL del mapa
        map_instance = get_filter_aestetic(valor)
        print(map_instance)
        if map_instance:
            # Enviar la URL a otro servicio
            send_map_url_to_serviceAE(map_instance.aestatic_file)
            return JsonResponse({'message': 'Gif enviado'})
    return JsonResponse({'message': 'Map type or state not set'})

def get_filter_aestetic(valor):
    # Utiliza las variables globales para filtrar el queryset
    slider_param = globals.aestatic_type

    queryset = AeStatic.objects.all()

    queryset = queryset.filter(
        slider=valor)
    # Obtén el mapa correspondiente (asumiendo que quieres el primero que coincida)
    aestatic_instance = queryset.first()
    return aestatic_instance if aestatic_instance else None

# envia un post al bug-free-train
def send_map_url_to_serviceAE(aestatic_url):
    # Implementa la lógica para enviar la URL a otro servicio
    print(aestatic_url.name)
    base_url = 'http://bug-free-train-backend-1:5000'
    endpoint = 'post-image'
    response = requests.post(f'{base_url}/{endpoint}', json={'url': aestatic_url.name})
    print(response.status_code)