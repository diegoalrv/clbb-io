from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from backend.services.layer import read_layer_data, read_layer_limits

import pandas as pd
import geopandas as gpd

# import matplotlib.pyplot as plt
# import matplotlib.colors as colors

# cvals  = [0, 0.25, 0.5, 0.75, 1]
# colors = [
#     '#3C1877',
#     '#5F28B8',
#     '#5A5CD3',
#     '#53D1E4',
#     '#80FFDB'
# ]

# norm=plt.Normalize(min(cvals), max(cvals))
# tuples = list(zip(map(norm, cvals), colors))

# cmap = plt.cm.get_cmap('viridis')
# cmap = matplotlib.colors.LinearSegmentedColormap.from_list('', tuples)

# def get_color(self, value, vmin, vmax, alpha, cmap):
#     norm = plt.Normalize(vmin, vmax)
#     color = cmap(norm(value))
#     return [int(color[0] * 255), int(color[1] * 255), int(color[2] * 255), int(alpha)]

from .models import (
    GlobalVariable,
    Layer,
    State,
    Selection,
    Option,
    LayerSelection,
    Colormap,
    Data,
    LayerData,
    Texture,
)

from .serializers import (
    GlobalVariableSerializer,
    LayerSerializer,
    StateSerializer,
    SelectionSerializer,
    OptionSerializer,
    LayerSelectionSerializer,
    ColormapSerializer,
    DataSerializer,
    LayerDataSerializer,
    TextureSerializer
    # ConfigSerializer
)

class GlobalVariableViewSet(viewsets.ModelViewSet):
    queryset = GlobalVariable.objects.all()
    serializer_class = GlobalVariableSerializer

class LayerViewSet(viewsets.ModelViewSet):
    queryset = Layer.objects.all()
    serializer_class = LayerSerializer

    def list(self, request):
        layers = Layer.objects.all()
        serialized = LayerSerializer(layers, many=True).data
        return Response(serialized)

    @action(detail=True, methods=['get'])
    def data(self, request, pk):
        try:
            layer = Layer.objects.get(id=pk)
            key = request.GET.get('key', 'data')
            data = layer.data.filter(key=key).first()  # related_name='data'
            return read_layer_data(data)
        except:
            return JsonResponse({'status': 'error', 'message': 'An error has ocurred'})
    
    @action(detail=True, methods=['get'])
    def limits(self, request, pk):
        try:
            column_id = int(request.GET.get('columnId', 0))
            print('column_id: ', column_id)
            layer = Layer.objects.get(id=pk)
            print('layer: ', layer)
            print('modules: ', layer.config.first().modules)
            column = layer.config.first().modules.get('column', {}).get('columns', ['value'])[column_id]
            print('column: ', column)
            # key = request.GET.get('key', 'data')
            key = 'data'
            print('key: ', key)
            data = layer.data.filter(key=key).first()  # related_name='data'
            print('data: ', data)
            vmin, vmax = read_layer_limits(data, column)
            print('vmin: ', vmin, 'vmax', vmax)
            return JsonResponse({'status': 'ok', 'vmin': vmin, 'vmax': vmax})
        except:
            return JsonResponse({'status': 'error', 'message': 'An error has ocurred'})

class DataViewSet(viewsets.ModelViewSet):
    queryset = Data.objects.all()
    serializer_class = DataSerializer

# class TextureViewSet(viewsets.ModelViewSet):
    # queryset = Texture.objects.all()

# class ConfigViewSet(viewsets.ModelViewSet):
#     queryset = Config.objects.all()
#     serializer_class = ConfigSerializer

class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer

class SelectionViewSet(viewsets.ModelViewSet):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer

class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer

class LayerSelectionViewSet(viewsets.ModelViewSet):
    queryset = LayerSelection.objects.all()
    serializer_class = LayerSelectionSerializer

class ColormapViewSet(viewsets.ModelViewSet):
    queryset = Colormap.objects.all()
    serializer_class = ColormapSerializer

class LayerDataViewSet(viewsets.ModelViewSet):
    queryset = LayerData.objects.all()
    serializer_class = LayerDataSerializer

    @action(detail=True, methods=['get'])
    def read(self, request, pk):
        instance = LayerData.objects.get(pk=pk)
        return read_layer_data(instance)

class TextureViewSet(viewsets.ModelViewSet):
    queryset = Texture.objects.all()
    serializer_class = TextureSerializer

# Now lets program the views for the API as an interactive platform

from . import globals
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class CustomActionsViewSet(viewsets.ViewSet):
    def check_and_send_message(self, message):
        # Si la condición es válida, enviamos los datos a los consumidores
        channel_layer = get_channel_layer()
        print(message)

    @action(detail=False, methods=['get'])
    def get_layers_state(self, request):
        return JsonResponse({})