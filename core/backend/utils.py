import geopandas as gpd
import json

def file_to_geojson(file_field):
    """
    Reads a file from a Django FileField and returns a GeoJSON dictionary.

    Args:
        file_field: A Django FileField instance (e.g., LayerData.file).

    Returns:
        dict: GeoJSON representation of the file contents, or
        dict with "error" key if reading fails.
    """
    try:
        # If the file is saved locally, you can use file_field.path
        # If not, you may need to open the file differently
        gdf = gpd.read_file(file_field.path)

        geojson_dict = gdf.to_geo_dict()

        return geojson_dict
    except Exception as e:
        return {"error": str(e)}