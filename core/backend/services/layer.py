import geopandas as gpd
import json
import os

from backend.models import Config

def set_layer_visibility(layer_id: int, on: bool):
    try:
        layer_config = Config.objects.get(id=layer_id)
        if not layer_config.config:
            layer_config.config = {}
        layer_config.config['on'] = on
        layer_config.save()
        return layer_config
    except Config.DoesNotExist:
        return None

# currently not being used as tests were made only for visibility
def set_layer_config(layer_id: int, config: dict):
    try:
        layer_config = Config.objects.get(id=layer_id)
        if not layer_config.config:
            layer_config.config = {}
        layer_config.config = {**layer_config.config, **config}
        layer_config.save()
        return layer_config
    except Config.DoesNotExist:
        return None

def read_layer_data(data):
    try:
        file_path = data.file.path
        print(file_path)

        if data.layer.type == 'geojson':
            gdf = gpd.read_parquet(file_path)

            try:
                assert 'cmap' in data.config.processing_props.keys()
                assert 'column' in data.config.processing_props.keys()
                assert data.config.processing_props['column'] in gdf.columns

                gdf['color'] = [255, 255, 255, 255]
            except:
                pass

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