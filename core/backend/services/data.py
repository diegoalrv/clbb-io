import geopandas as gpd
import json
import os

from backend.models import Layer, Config, Data
import matplotlib.pyplot as plt
import numpy as np

from django.http import FileResponse
from rest_framework.response import Response

# def set_layer_visibility(layer_id: int, on: bool):
#     try:
#         config = Config.objects.get(id=layer_id)
#         if not config.config:
#             config.config = {}
#         config.config['on'] = on
#         config.save()
#         return config
#     except Config.DoesNotExist:
#         return None

# currently not being used as tests were made only for visibility
def set_config(layer_id: int, content: dict):
    try:
        config = Config.objects.get(layer__id=layer_id)
        print("layer_id", layer_id)
        print("config", config)

        print("config.modules before", config.modules)
        for module_key, module in content.get('modules', {}).items():
            print("module", module_key)
            if config.modules[module_key]:
                print("already has module", module_key)
                for property_key, property in module.items():
                    print("property", property_key)
                    config.modules[module_key][property_key] = property
            else:
                print("it had not module", module_key)
                config.modules[module_key] = module

        # config.props = {**config.props, **content.props}

        config.save()
        print("config.modules after", config.modules)
        return config
    except Config.DoesNotExist:
        return None

def apply_colormap(gdf, column, colormap='viridis', vmin=None, vmax=None):
    values = gdf[column].astype(float)
    vmin = vmin if vmin is not None else values.min()
    vmax = vmax if vmax is not None else values.max()

    print(vmin, vmax)
    
    cmap = plt.get_cmap(colormap)
    norm = plt.Normalize(vmin=vmin, vmax=vmax)
    colors = [cmap(norm(val)) for val in values]
    gdf['color'] = [(int(r * 255), int(g * 255), int(b * 255), int(a * 255)) for r, g, b, a in colors]
    return gdf

def read_layer_limits(data):
    try:
        file_path = data.file.path
        gdf = gpd.read_parquet(file_path)
        
        colormap = data.layer.config.first().modules.get('colormap', {})
        column = colormap.get('column', 'value')
        vmin = gdf[column].min()
        vmax = gdf[column].max()

        return vmin, vmax
    except:
        return None, None

def read_layer_data(data):
        file_path = data.file.path

        gdf = gpd.GeoDataFrame()
        json_data = None

        print('# Data reading')
        # Data reading
        if data.props.get('filetype') == 'parquet':
            print('parquet')
            gdf = gpd.read_parquet(file_path)
        elif data.props.get('filetype') == 'shapefile':
            print('shapefile')
            gdf = gpd.read_file(file_path)
        elif data.props.get('filetype') == 'json':
            print('json')
            with open(file_path) as f:
                json_data = json.load(f)
        elif data.props.get('filetype') == 'bin':
            print('bin')
            return FileResponse(open(file_path, 'rb'), content_type='application/octet-stream')

        print('# Module processing')
        # Module processing
        if not gdf.empty:
            colormap = data.layer.config.first().modules.get('colormap', {})
            column = colormap.get('column', 'value')
            cmap = colormap.get('cmap')
            vmin = colormap.get('vmin')
            vmax = colormap.get('vmax')
            gdf = apply_colormap(gdf, column, cmap, vmin, vmax)

        print('# Response')
        # Response
        if data.layer.type == 'geojson':
            return Response(gdf.to_geo_dict())
        else:
            return Response(json_data)

# def get_layer_binary(request, layer_id):
#     data = Data.objects.get(layer_id=layer_id)

#     if data.props.get('filetype') != 'bin':
#         return JsonResponse({'error': 'Not a binary file'}, status=400)

#     file_path = data.file.path
#     return FileResponse(open(file_path, 'rb'), content_type='application/octet-stream')