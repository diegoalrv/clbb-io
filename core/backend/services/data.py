import geopandas as gpd
import json
import os

from backend.models import Config
import matplotlib.pyplot as plt
import numpy as np

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

def read_layer_data(data):
    try:
        file_path = data.file.path
        print(file_path)

        if data.layer.type == 'geojson':
            gdf = gpd.read_parquet(file_path)

            try:
                colormap_module = data.layer.config.first().modules.get('colormap', {})
                
                column = colormap_module.get('column', 'value')
                cmap = colormap_module.get('cmap')
                vmin = colormap_module.get('vmin')
                vmax = colormap_module.get('vmax')
                
                gdf = apply_colormap(gdf, column, cmap, vmin, vmax)
            except:
                print('Exception ocurred setting color')

            return gdf.to_geo_dict()
        if data.layer.type == 'trips':
            with open(file_path) as f:
                geojson = json.load(f)
            return geojson
        else:
            return None  # Or raise NotImplementedError

    except Exception as e:
        print(f"Failed to read file for layer {data.id}: {e}")
        return None