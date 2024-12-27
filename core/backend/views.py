from django.shortcuts import render
from django.db import models
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
import json

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

from . import globals
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class CustomActionsViewSet(viewsets.ViewSet):

    def check_and_send_data(self):
        # Si la condición es válida, enviamos los datos a los consumidores
        channel_layer = get_channel_layer()
        message = {
            'indicator_id': globals.INDICATOR_ID,
            'indicator_state': globals.INDICATOR_STATE
        }
        print(message)
    
    @action(detail=False, methods=['get'])
    def get_global_variables(self, request):
        return JsonResponse({
            'indicator_id': globals.INDICATOR_ID,
            'indicator_state': globals.INDICATOR_STATE
        })

    @action(detail=False, methods=['post'])
    def set_current_indicator(self, request):
        indicator_id = request.data.get('indicator_id', '')
        if self._set_current_indicator(indicator_id):
            return JsonResponse({'status': 'ok', 'indicator_id': indicator_id})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to set current indicator'})
    
    def _set_current_indicator(self, indicator_id):
        try:
            globals.INDICATOR_ID = indicator_id
            self.check_and_send_data()
            return True
        except Exception as e:
            print(e)
            return False

    @action(detail=False, methods=['post'])
    def set_current_state(self, request):
        state = request.data.get('state', '')
        if isinstance(state, str):
            state = json.loads(state)
        if self._set_current_state(state):
            return JsonResponse({'status': 'ok', 'state': state})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to set current state'})

    def _set_current_state(self, state):
        try:
            globals.INDICATOR_STATE = state
            self.check_and_send_data()
            return True
        except Exception as e:
            print(e)
            return False

    @action(detail=False, methods=['get'])
    def receive_data_from_rfid(self, request):
        slots_param = request.GET.get('slots', '')
        keys = globals.INDICATOR_STATE.keys()
        states = {f"{key}": 0 for key in keys}
        if slots_param:
            print('list_temp ', globals.SLOTS_IDS)
            rfid_tags = sorted(slots_param.split(','))
            if(len(rfid_tags) != len(globals.SLOTS_IDS)):
                print(f'Number of tags reported: {len(rfid_tags)}')
            else:
                for pos, rfid_tag in enumerate(rfid_tags):
                    (SLOT, STATE) = globals.SLOTS_IDS[rfid_tag]
                    states[f'{SLOT}'] = STATE
                
                self._set_current_state(states)
                # if self._set_current_state(states):
                    # return JsonResponse({'status': 'ok', 'states': states})
                # else:
                    # return JsonResponse({'status': 'error', 'message': 'Failed to set current state'})

    @action(detail=False, methods=['get'])
    def receive_data_from_buttons_page(self, request):
        print(request.body)
        if request.method == 'GET':
            type_param = request.GET.get('map_type', 1)
            self._set_current_indicator(type_param)

    @action(detail=False, methods=['get'])
    def get_image_data(self, request):
        indicator = Indicator.objects.filter(indicator_id=globals.INDICATOR_ID)
        if(indicator.first().has_states == False):
            state = State.objects.filter(state_values={})
        else:
            state = State.objects.filter(state_values=globals.INDICATOR_STATE)
        
        indicator_data = IndicatorData.objects.filter(
            indicator=indicator.first(),
            state=state.first()
        )

        image_data = IndicatorImage.objects.filter(indicatorData=indicator_data.first())
        return JsonResponse({'image_data': image_data.first().image.name})

    @action(detail=False, methods=['get'])
    def get_geojson_data(self, request):
        indicator = Indicator.objects.filter(indicator_id=globals.INDICATOR_ID)
        if(indicator.first().has_states == False):
            state = State.objects.filter(state_values={})
        else:
            state = State.objects.filter(state_values=globals.INDICATOR_STATE)
        
        indicator_data = IndicatorData.objects.filter(
            indicator=indicator.first(),
            state=state.first()
        )
        geojson_data = IndicatorGeojson.objects.filter(indicatorData=indicator_data.first())
        return JsonResponse({'geojson_data': geojson_data.first().geojson})

    @action(detail=False, methods=['get'])
    def get_current_dashboard_data(self, request):
        state = State.objects.filter(state_values=globals.INDICATOR_STATE)
        dashboard_data = DashboardFeedState.objects.filter(
            state=state.first()
        ).first()
        return JsonResponse({'data': dashboard_data.data, 'state': state.first().state_values})
