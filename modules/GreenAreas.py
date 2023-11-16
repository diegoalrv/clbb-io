import geopandas as gpd
import numpy as np
import pandas as pd
from glob import glob
from modules.Base import BaseModule

class GreenAreas(BaseModule):
    def __init__(self) -> None:
        super().__init__()
        self.cols = ['ID_AV', 'ID_PLACA', 'geometry']
        self.scenarios_status = [0]*self.num_plates
        self.load_data()
        pass

    def load_data(self):
        self.scenarios = []
        [self.scenarios.append(gpd.read_file(file)[self.cols].to_crs(self.default_crs)) for file in glob('/app/assets/green_areas/*')]
        [gdf['ID_PLACA'].fillna(0, inplace=True) for gdf in self.scenarios];
        self.current_scenario = self.scenarios[0]
        pass

    def update_plate_area(self, plate_id, scenario_id):
        mask = self.current_scenario['ID_PLACA'] == plate_id
        self.current_scenario = self.current_scenario[~mask]

        new_scenario = self.scenarios[scenario_id]
        mask = new_scenario['ID_PLACA'] == plate_id
        new_scenario = new_scenario[mask]
        
        self.current_scenario = pd.concat([self.current_scenario, new_scenario])
        pass

    def get_green_areas_ids(self):
        return list(self.current_scenario['ID_AV'].unique())
    
    def get_green_area_by_id(self, green_area_id):
        mask = (self.current_scenario['ID_AV'].isin([green_area_id]))
        return self.current_scenario[mask]
    
    def get_countour_by_id(self, green_area_id):
        return list(self.get_green_area_by_id(green_area_id).iloc[0]['geometry'].exterior.coords)
    
    def get_green_areas(self):
        return self.current_scenario