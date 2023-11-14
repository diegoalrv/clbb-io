import pandas as pd
import geopandas as gpd
import numpy as np


class BaseModule():
    def __init__(self) -> None:
        self.default_crs = '32718'
        pass