from django.shortcuts import render
from django.db import models
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import (
    Indicator, IndicatorData, IndicatorImage, IndicatorGeojson,
    State, DashboardFeedState, LayerConfig
)

from .serializers import (
    IndicatorSerializer, IndicatorDataSerializer, IndicatorImageSerializer,
    IndicatorGeojsonSerializer, StateSerializer, DashboardFeedStateSerializer,
    StateSerializer, LayerConfigSerializer
)

class IndicatorViewSet(viewsets.ModelViewSet):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer

class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer

class IndicatorDataViewSet(viewsets.ModelViewSet):
    queryset = IndicatorData.objects.all()
    serializer_class = IndicatorDataSerializer

class IndicatorImageViewSet(viewsets.ModelViewSet):
    queryset = IndicatorImage.objects.all()
    serializer_class = IndicatorImageSerializer

class IndicatorGeojsonViewSet(viewsets.ModelViewSet):
    queryset = IndicatorGeojson.objects.all()
    serializer_class = IndicatorGeojsonSerializer

class DashboardFeedStateViewSet(viewsets.ModelViewSet):
    queryset = DashboardFeedState.objects.all()
    serializer_class = DashboardFeedStateSerializer

class LayerConfigViewSet(viewsets.ModelViewSet):
    queryset = LayerConfig.objects.all()
    serializer_class = LayerConfigSerializer

# Now lets program the views for the API as an interactive platform

from .globals import (
    INDICATOR_STATE, INDICATOR_ID, SLOTS_IDS
)

@action(detail=False, methods=['get'])
def check_and_send_data(request):
    # Send data to all current clients connected to the server using websocket

    return JsonResponse({'status': 'ok'})
    # channel_layer = get_channel_layer()
    # async_to_sync(channel_layer.group_send)(
    #     'clients_group',
    #     {
    #         'type': 'send_data',
    #         'message': 'Data to be sent to clients'
    #     }
    # )


    pass

# I should be able to set the id of the current state of the interface
@action(detail=False, methods=['post'])
def set_current_indicator(request, indicator_id):
    INDICATOR_ID = indicator_id
    return JsonResponse({'status': 'ok'})

# I should be able to set the id of an indicator that i want
@action(detail=False, methods=['post'])
def set_current_state(request, state):
    INDICATOR_STATE = state
    return JsonResponse({'status': 'ok'})

# I should be able to receive data from the RFID
@action(detail=False, methods=['get'])
def receive_data_from_rfid(request):
    slots_param = request.GET.get('slots', '')
    if slots_param:
        print('list_temp ',globals.list_temp)
        rfid_tags = sorted(slots_param.split(','))
    # I should be able to receive data from the RFID and set the current state of the interface
    for rfid_tag in rfid_tags:
        (SLOT, STATE) = SLOTS_IDS[rfid_tag]
        INDICATOR_ID[SLOT] = STATE
    return JsonResponse({'status': 'ok'})

# I should request for the image data of the current indicator-state pair
@action(detail=False, methods=['get'])
def get_image_data(request):
    indicator = Indicator.objects.get(id=INDICATOR_ID)
    if not indicator.has_state:
        image_data = IndicatorImage.objects.get(indicator=indicator)
    else:
        state = State.objects.get(name=INDICATOR_STATE)
        image_data = IndicatorImage.objects.get(indicator=indicator, state=state)
    return JsonResponse({'image_data': image_data})

# I should be able to request for the geojson data of the current indicator-state pair
@action(detail=False, methods=['get'])
def get_geojson_data(request):
    indicator = Indicator.objects.get(id=INDICATOR_ID)
    state = State.objects.get(name=INDICATOR_STATE)
    if not indicator.has_state:
        geojson_data = IndicatorImage.objects.get(indicator=indicator)
    else:
        state = State.objects.get(name=INDICATOR_STATE)
        geojson_data = IndicatorImage.objects.get(indicator=indicator, state=state)
    return JsonResponse({'geojson_data': geojson_data.get()})