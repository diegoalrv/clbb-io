import geopandas as gpd
import numpy as np
import pandas as pd
from glob import glob
from modules.Base import BaseModule

class Blocks(BaseModule):
    def __init__(self, as_unit=False) -> None:
        super().__init__()
        self.cols = ['block_id', 'q_residents', 'ID_PLACA']
        self.scenarios_status = [0]*self.num_plates
        self.as_unit = as_unit
        self.as_variable = ~as_unit
        self.node_set = None
        self.load_data()
        pass

    def load_data(self):
        self.scenarios = []
        [self.scenarios.append(gpd.read_parquet(file).to_crs(self.default_crs)) for file in glob('/app/assets/blocks/*')]
        self.current_scenario = self.scenarios[0]
        pass

    def get_current_scenario(self):
        return self.current_scenario