import geopandas as gpd
import json
import os

from backend.models import LayerConfig

def set_layer_visibility(layer_id: int, on: bool):
    try:
        layer_config = LayerConfig.objects.get(id=layer_id)
        if not layer_config.config:
            layer_config.config = {}
        layer_config.config['on'] = on
        layer_config.save()
        return layer_config
    except LayerConfig.DoesNotExist:
        return None

# currently not being used as tests were made only for visibility
def set_layer_config(layer_id: int, config: dict):
    try:
        layer_config = LayerConfig.objects.get(id=layer_id)
        if not layer_config.config:
            layer_config.config = {}
        layer_config.config = {**layer_config.config, **config}
        layer_config.save()
        return layer_config
    except LayerConfig.DoesNotExist:
        return None

def read_layer_file(layer_data_obj, layer_type):
    try:
        file_path = layer_data_obj.file.path
        print(file_path)

        if layer_type == 'geojson':
            gdf = gpd.read_parquet(file_path)
            return gdf.to_geo_dict()
        if layer_type == 'trips':
            with open(file_path) as f:
                geojson = json.load(f)
            return geojson
        else:
            return None  # Or raise NotImplementedError

    except Exception as e:
        print(f"Failed to read file for layer {layer_data_obj.id}: {e}")
        return None