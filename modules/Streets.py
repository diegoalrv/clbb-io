import geopandas as gpd
import numpy as np
import pandana as pdna
import pandas as pd
from glob import glob
import matplotlib.pyplot as plt
from modules.Base import BaseModule

import warnings
warnings.filterwarnings("ignore")

class Streets(BaseModule):
    def __init__(self) -> None:
        super().__init__()
        self.nodes_cols = []
        self.edges_cols = []
        self.scenarios_status = [0]*self.num_plates
        self.load_data()
        pass

    def load_data(self):
        self.scenarios = []
        [
            self.scenarios.append({
                    # 'nodes': gpd.read_file(node_file).to_crs(self.default_crs),
                    # 'edges': gpd.read_file(edge_file).to_crs(self.default_crs)
                    'nodes': gpd.read_parquet(node_file),
                    'edges': gpd.read_parquet(edge_file)
            })
            for node_file, edge_file in zip(
                glob('/app/assets/streets/*/nodes.parquet'),
                glob('/app/assets/streets/*/edges.parquet')
                )
        ]
        # Assume that the baseline is in index 0
        self.current_scenario = self.scenarios[0]
        self._make_network()
        pass

    def go_to_scenario(self, scenario_id):
        self.current_scenario = self.scenarios[scenario_id]
        self._make_network()
        self.scenarios_status = [scenario_id]*self.num_plates
        pass

    def update_network(self, plate_id, scenario_id):
        self._update_plate_area(plate_id=plate_id, scenario_id=scenario_id)
        self._make_network()
        self.scenarios_status[plate_id] = scenario_id
        pass

    def _update_plate_area(self, plate_id, scenario_id):
        # Change the nodes and edges within the area into plate

        current_nodes = self.current_scenario['nodes']
        current_edges = self.current_scenario['edges']

        update_nodes = self.scenarios[scenario_id]['nodes']
        update_edges = self.scenarios[scenario_id]['edges']

        mask_current_nodes = current_nodes['plate_id'] != plate_id
        mask_current_edges = current_edges['plate_id'] != plate_id

        mask_update_nodes = update_nodes['plate_id'] == plate_id
        mask_update_edges = update_edges['plate_id'] == plate_id
        
        edges_updated = pd.concat([
            current_edges[mask_current_edges],
            update_edges[mask_update_edges]
            ]).drop_duplicates(subset=['u', 'v', 'key'])
        
        # Fix missing nodes
        look_nodes = list(edges_updated['u'].values) + list(edges_updated['v'].values)
        
        fixed_current_nodes = current_nodes[
            current_nodes['osmid'].isin(look_nodes)
        ]

        fixed_update_nodes = update_nodes[
            update_nodes['osmid'].isin(look_nodes)
        ]

        # Clean duplicates
        nodes_updated = pd.concat([
            current_nodes[mask_current_nodes],
            update_nodes[mask_update_nodes],
            fixed_current_nodes,
            fixed_update_nodes,
        ]).drop_duplicates(subset=['osmid'])
        
        # Only nodes with edges connected
        nodes_updated = nodes_updated[
            nodes_updated['osmid'].isin(edges_updated['u']) | nodes_updated['osmid'].isin(edges_updated['v'])
        ]

        self.current_scenario = {
            'nodes': gpd.GeoDataFrame(data=nodes_updated.drop(columns=['geometry']), geometry=nodes_updated['geometry']),
            'edges': gpd.GeoDataFrame(data=edges_updated.drop(columns=['geometry']), geometry=edges_updated['geometry']),
        }
        pass

    def _current_nodes_edges_to_net_format(self):
        nodes_df = self.current_scenario['nodes']
        edges_df = self.current_scenario['edges']

        nodes = pd.DataFrame(
            {
                'osmid': nodes_df['osmid'].astype(int),
                'lat' : nodes_df.geometry.y.astype(float),
                'lon' : nodes_df.geometry.x.astype(float),
                'y' : nodes_df.geometry.y.astype(float),
                'x' : nodes_df.geometry.x.astype(float),
            }
        )
        nodes['id'] = nodes['osmid'].values

        nodes = gpd.GeoDataFrame(data=nodes, geometry=nodes_df.geometry)
        nodes.set_index('osmid', inplace=True)
        nodes.drop_duplicates(inplace=True)

        edges = pd.DataFrame(
            {
                'u': edges_df['u'].astype(int),
                'v': edges_df['v'].astype(int),
                'from': edges_df['u'].astype(int),
                'to': edges_df['v'].astype(int),
                'osmid': edges_df['osmid'].astype(int),
                'length': edges_df['length'].astype(float)
            }
        )
        edges['key'] = 0
        edges['key'] = edges['key'].astype(int)
        edges = gpd.GeoDataFrame(data=edges, geometry=edges_df.geometry)
        edges.set_index(['u', 'v', 'key'], inplace=True)
        edges.drop_duplicates(inplace=True)
        return nodes, edges
    
    def _make_network(self):
        nodes, edges = self._current_nodes_edges_to_net_format()
        self.current_scenario['net'] = pdna.Network(
            nodes['lon'],
            nodes['lat'],
            edges['from'],
            edges['to'],
            edges[['length']]
        )
        pass

    def get_current_nodes_and_edges(self):
        return self.current_scenario['nodes'], self.current_scenario['edges']
    
    def get_current_scenario_status(self):
        return self.scenarios_status