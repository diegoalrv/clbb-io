import geopandas as gpd
import numpy as np
import pandas as pd
from glob import glob
from modules.Base import BaseModule

class LandUses(BaseModule):
        def __init__(self) -> None:
            super().__init__()
            self.cols = ['Id', 'Uso', 'area_predio', 'geometry']
            self.scenarios_status = [0]*self.num_plates
            self.load_data()
            pass

        def load_data(self):
            self.scenarios = []
            [self.scenarios.append(gpd.read_parquet(file).to_crs(self.default_crs)) for file in glob('/app/assets/land_uses/*.parquet')]
            # [gdf['ID_PLACA'].fillna(0, inplace=True) for gdf in self.scenarios];
            self.current_scenario = self.scenarios[0]
            pass

        def update_plate_area(self, plate_id, scenario_id):
            # mask = self.current_scenario['ID_PLACA'] == plate_id
            # self.current_scenario = self.current_scenario[~mask]

            # new_scenario = self.scenarios[scenario_id]
            # mask = new_scenario['ID_PLACA'] == plate_id
            # new_scenario = new_scenario[mask]
            
            # self.current_scenario = pd.concat([self.current_scenario, new_scenario])
            pass

        def get_current_land_uses(self):
             return self.current_scenario

        def go_to_scenario(self, scenario_id):
            self.current_scenario = self.scenarios[scenario_id]
            pass