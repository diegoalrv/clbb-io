from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from backend.services.data import read_layer_data, read_layer_limits

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
    # Texture,
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
        refresh_limits = request.GET.get('limits') == 'true'

        layers = Layer.objects.all()
        response_data = []

        for layer in layers:
            serialized = LayerSerializer(layer).data

            if include_data:
                data_objs = layer.data.all()  # related_name='data'
                serialized_data_objs = DataSerializer(data_objs, many=True).data
                print('serialized_data_objs', serialized_data_objs)
                # serialized_data_objs = []

                # for data in data_objs:
                #     serialized_data_objs.append({
                #         'key': f'http://localhost:9900/api/layer/{layer.id}/data/?key={data.key}'
                #         'url': f'http://localhost:9900/api/layer/{layer.id}/data/?key={data.key}'
                #     })
                serialized['data'] = [{
                    'id': obj['id'],
                    'key': obj['key'],
                    'type': obj['type'],
                    'props': obj['props'],
                    'url': f'http://localhost:9900/api/data/{obj["id"]}/data/'
                } for obj in serialized_data_objs]

            if include_config:
                config = layer.config.first()  # related_name='config'
                try:
                    assert config
                    colormap = config.modules.get('colormap')

                    assert colormap
                    vmin, vmax = read_layer_limits(layer.data.first())
                    config.modules['colormap'] = {
                        **config.modules['colormap'],
                        'vmin': {
                            **config.modules['colormap']['vmin'],
                            'default': vmin,
                        },
                        'vmax': {
                            **config.modules['colormap']['vmax'],
                            'default': vmax,
                        }
                    }
                    config.save()
                except:
                    pass

                serialized['modules'] = config.modules
                serialized['props'] = config.props

                # serialized_config = ConfigSerializer(config).data
                # serialized['config'] = serialized_config
                # del serialized['config']['id']
                # del serialized['config']['layer']

            response_data.append(serialized)

        return Response(response_data)
    
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

    @action(detail=True, methods=['get'])
    def data(self, request, pk):
        instance = Data.objects.get(pk=pk)
        return read_layer_data(instance)

# class TextureViewSet(viewsets.ModelViewSet):
    # queryset = Texture.objects.all()

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