import pandas as pd
import geopandas as gpd
import numpy as np
import glob
import os

class BaseModule():
    def __init__(self) -> None:
        self.default_crs = '32718'
        self.load_plates()
        self.load_area_scope()
        pass

    def load_plates(self):
        plates_path = '/app/assets/plates'
        plates_files = glob.glob(os.path.join(plates_path, '*'))
        self.plates = {}
        for file in plates_files:
            idx = os.path.split(file)[-1]
            plate = gpd.read_file(file).to_crs(self.default_crs)
            self.plates[idx] = plate
        pass

    def load_area_scope(self):
        area_scope_path = '/app/assets/area_scope'
        self.area_scope = gpd.read_file(area_scope_path)
        pass