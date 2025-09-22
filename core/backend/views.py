from django.shortcuts import render
from django.db import models
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
import json

from backend.services.layer import read_layer_file

# import pandas as pd
# import geopandas as gpd
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
    LayerData,
    LayerConfig
)

from .serializers import (
    LayerSerializer,
    LayerDataSerializer,
    LayerConfigSerializer
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
                    serialized['data'] = read_layer_file(data, layer.type)

            if include_config:
                config = layer.config.first()  # related_name='config'
                if config:
                    serialized['config'] = config.config

            response_data.append(serialized)

        return Response(response_data)

class LayerDataViewSet(viewsets.ModelViewSet):
    queryset = LayerData.objects.all()
    serializer_class = LayerDataSerializer

class LayerConfigViewSet(viewsets.ModelViewSet):
    queryset = LayerConfig.objects.all()
    serializer_class = LayerConfigSerializer

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