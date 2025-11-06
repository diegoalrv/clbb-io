import geopandas as gpd
import json
import os

from backend.models import Layer, Data
import matplotlib.pyplot as plt
import numpy as np

from django.http import FileResponse
from rest_framework.response import Response

def set_layer_visibility(layer_id: int, on: bool):
    try:
        config = Layer.objects.get(id=layer_id)
        config.on = on
        config.save()
        return config
    except Layer.DoesNotExist:
        return None
    
def set_layer_state(layer_id: int, new_state: dict):
    try:
        layer = Layer.objects.get(id=layer_id)
        state = layer.state

        for key, value in new_state.items():
            if hasattr(state, key) and key != 'layer':
                setattr(state, key, value)

        state.save()
        return state
    except Layer.DoesNotExist:
        return None
    
def set_layer_colormap(layer_id: int, new_colormap: dict):
    try:
        layer = Layer.objects.get(id=layer_id)
        colormap = layer.colormap

        for key, value in new_colormap.items():
            if hasattr(colormap, key) and key != 'layer':
                setattr(colormap, key, value)

        colormap.save()
        return colormap
    except Layer.DoesNotExist:
        return None

# # currently not being used as tests were made only for visibility
# def set_config(layer_id: int, content: dict):
#     try:
#         config = Config.objects.get(layer__id=layer_id)

#         for module_key, module in content.get('modules', {}).items():
#             if config.modules[module_key]:
#                 for property_key, property in module.items():
#                     config.modules[module_key][property_key] = property
#             else:
#                 config.modules[module_key] = module

#         # config.props = {**config.props, **content.props}

#         config.save()
#         return config
#     except Config.DoesNotExist:
#         return None

def apply_colormap(gdf, column, colormap='viridis', vmin=None, vmax=None):
    values = gdf[column].astype(float)
    vmin = vmin if vmin is not None else values.min()
    vmax = vmax if vmax is not None else values.max()

    cmap = plt.get_cmap(colormap)
    norm = plt.Normalize(vmin=vmin, vmax=vmax)
    colors = [cmap(norm(val)) for val in values]
    gdf['color'] = [(int(r * 255), int(g * 255), int(b * 255), int(a * 255)) for r, g, b, a in colors]
    return gdf

def read_layer_limits(data, pass_column=None):
    print('pass_column: ', pass_column)
    try:
        file_path = data.file.path

        if data.props.get('filetype') == 'parquet':
            gdf = gpd.read_parquet(file_path)

            try:
                column_module = data.layer.config.first().modules.get('column', {})
                column = column_module['columns'][column_module['selected']]
            except:
                column = 'value'

            vmin = gdf[column if pass_column == None else pass_column].min()
            vmax = gdf[column if pass_column == None else pass_column].max()
        elif data.props.get('filetype') == 'shapefile':
            gdf = gpd.read_file(file_path)

            try:
                column_module = data.layer.config.first().modules.get('column', {})
                column = column_module['columns'][column_module['selected']]
            except:
                column = 'value'

            vmin = gdf[column if pass_column == None else pass_column].min()
            vmax = gdf[column if pass_column == None else pass_column].max()
        elif data.props.get('filetype') == 'json':
            with open(file_path) as f:
                json_data = json.load(f)
            
            print('name', data.layer.name, 'type', data.layer.type)
            if data.layer.type == 'h3':
                column_module = data.layer.config.first().modules.get('column', {})
                column = column_module['columns'][column_module['selected']]
                
                day_module = data.layer.config.first().modules.get('day', {})
                day = day_module['options'][day_module['selected']]

                values_arr = np.array([d['values'][day][0][column if pass_column == None else pass_column] for d in json_data])
                vmin = values_arr.min()
                vmax = values_arr.max()
                print(vmin, vmax)

        elif data.props.get('filetype') == 'bin':
            return FileResponse(open(file_path, 'rb'), content_type='application/octet-stream')

        return vmin, vmax
    except:
        return None, None

def read_layer_data(layer_data):
        file_path = layer_data.data.file.path

        gdf = gpd.GeoDataFrame()
        json_data = None

        # Data reading
        if layer_data.data.type == 'parquet':
            gdf = gpd.read_parquet(file_path)

            first = layer_data.props.get('first')
            if isinstance(first, int):
                gdf = gdf.head(first)

            row = layer_data.props.get('row')
            if isinstance(row, int) and row < len(gdf):
                gdf = gdf.iloc[[row]]

        elif layer_data.data.type == 'shapefile':
            gdf = gpd.read_file(file_path)
        elif layer_data.data.type == 'json':
            with open(file_path) as f:
                json_data = json.load(f)
        elif layer_data.data.type == 'bin':
            return FileResponse(open(file_path, 'rb'), content_type='application/octet-stream')

        # Response
        if layer_data.layer.type == 'geojson':
            return Response(gdf.to_geo_dict())
        else:
            return Response(json_data)