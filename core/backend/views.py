from django.shortcuts import render
from django.db import models
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
import json

from backend.services.layer import read_layer_data

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
    Layer,
    Data,
    Config
)

from .serializers import (
    LayerSerializer,
    DataSerializer,
    ConfigSerializer
)

class LayerViewSet(viewsets.ModelViewSet):
    queryset = Layer.objects.all()
    serializer_class = LayerSerializer

    def list(self, request):
        include_data = request.GET.get('data') == 'true'
        include_config = request.GET.get('config') == 'true'

        layers = Layer.objects.all()
        response_data = []

        for layer in layers:
            serialized = LayerSerializer(layer).data

            if include_data:
                data = layer.data.first()  # related_name='data'
                if data:
                    serialized['data'] = read_layer_data(data, layer)
                else:
                    serialized['data'] = f'http://localhost:9900/api/layer/{layer.id}/data/'

            if include_config:
                config = layer.config.first()  # related_name='config'
                if config:
                    serialized['processing_props'] = config.processing_props
                    serialized['layer_props'] = config.layer_props

            response_data.append(serialized)

        return Response(response_data)
    
    @action(detail=True, methods=['get'])
    def data(self, request, pk):
        try:
            layer = Layer.objects.get(id=pk)
            data = layer.data.first()  # related_name='data'
            read_layer_data(data)
        except:
            return JsonResponse({'status': 'error', 'message': 'An error has ocurred'})
    
    # @action(detail=True, methods=['get'])
    # def data(self, request, pk):
    #     try:
    #         layer = Layer.objects.get(id=pk)
    #         data = Data.objects.get(layer=layer)
    #         config = Config.objects.get(layer=layer)
            
    #         gdf = gpd.read_parquet(data.file.file)
            
    #         cmap = plt.cm.get_cmap(config.get('color_map'))
    #         gdf['color'] = gdf['normalized'].apply(lambda c: colors.to_hex(cmap(c, True)))

    #         match layer.get('type'):
    #             case 'geojson':
    #                 return JsonResponse({'status': 'ok', 'message': 'Layer does not exist'})
    #                 to_path_data(gdf)
    #             case _:
    #                 pass

    #     except Layer.DoesNotExist as e:
    #         return JsonResponse({'status': 'error', 'message': 'Layer does not exist'})
    #     except Data.DoesNotExist as e:
    #         return JsonResponse({'status': 'error', 'message': 'Data does not exist for that layer'})
    #     except Config.DoesNotExist as e:
    #         return JsonResponse({'status': 'error', 'message': 'Config does not exist for that layer'})

class DataViewSet(viewsets.ModelViewSet):
    queryset = Data.objects.all()
    serializer_class = DataSerializer

    def retrieve(self, request, pk=None):
        queryset = Data.objects.all()
        data = get_object_or_404(queryset, pk=pk)
        json_data = read_layer_data(data)
        return Response(json_data)

class ConfigViewSet(viewsets.ModelViewSet):
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer

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