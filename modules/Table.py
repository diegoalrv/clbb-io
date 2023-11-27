import geopandas as gpd
import numpy as np
import pandas as pd
from glob import glob
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from .myfunctions import *
import itertools
from modules import Base, Streets, GreenAreas, Amenities, LandUses, Blocks, SidewalkMaterial

class TableUserInferface(Base.BaseModule):
    ######################################################################
    #### Funciones generales del modulo
    ######################################################################

    def __init__(self) -> None:
        super().__init__()
        self.st = Streets.Streets()
        self.ga = GreenAreas.GreenAreas()
        self.am = Amenities.Amenities()
        self.lu = LandUses.LandUses()
        self.bk = Blocks.Blocks()
        self.sm = SidewalkMaterial.SidewalkMaterial()
        self.modules_available = [
            'GreenAreas',
            'Streets',
            'Amenities',
            'LandUses',
            'Blocks',
        ]
        self.dict_scenarios = {
            0: 'actual',
            1: 'future',
        }
        self.present_scenario = 0
        self.load_unit()
        self.update_nodes_ids()

        self.numeric_kpis = {}

        pass

    def change_scenario(self, scenario_id):
        if self.present_scenario!=scenario_id:
            self.st.go_to_scenario(scenario_id)
            self.ga.go_to_scenario(scenario_id)
            self.am.go_to_scenario(scenario_id)
            self.lu.go_to_scenario(scenario_id)
            self.bk.go_to_scenario(scenario_id)
            self.update_nodes_ids()
            self.present_scenario=scenario_id
            if self.select_unit == 'block': self.load_unit(select_unit='block')
        pass

    def update_nodes_ids(self):
        self.calc_ga_node_ids()
        self.calc_am_node_ids()
        self.calc_unit_node_ids()
    
    def calc_heatmaps_kpis(self):
        if 'Amenities' in self.modules_available: self.calc_travel_time_to_amenities()
        if 'GreenAreas' in self.modules_available: self.calc_travel_time_to_green_areas()
        if 'LandUses' in self.modules_available: self.calc_land_uses_diversity()
        if 'Blocks' in self.modules_available: self.calc_population_density()
        pass

    def calc_numeric_kpis(self):
        if 'Amenities' in self.modules_available: pass
        if 'GreenAreas' in self.modules_available: pass
        if 'LandUses' in self.modules_available: pass
        if 'Blocks' in self.modules_available: pass
        pass 

    ######################################################################    
    #### Funciones de unidades espaciales
    ######################################################################

    def load_unit(self, select_unit='hex'):
        self.select_unit = select_unit
        if self.select_unit == 'block':
            filename = f'/app/assets/groupby/block/{self.dict_scenarios[self.present_scenario]}.parquet'
            unit = gpd.read_parquet(filename).to_crs(self.default_crs)
        else:
            unit = gpd.read_file(f'/app/assets/groupby/{self.select_unit}')
        unit['centroid'] = unit['geometry'].centroid
        unit['area'] = unit['geometry'].area
        self.unit = unit

        self.update_nodes_ids()
        pass

    def calc_unit_node_ids(self):
        self.unit['node_ids'] = self.st.current_scenario['net'].get_node_ids(
            self.unit['centroid'].x,
            self.unit['centroid'].y
        )
        pass
    

    ######################################################################
    #### Funciones para identificar nodos en lugares
    ######################################################################

    def calc_am_node_ids(self):
        self.am.node_set = self.am.current_scenario.copy()
        self.am.node_set['node_ids'] = self.st.current_scenario['net'].get_node_ids(
            self.am.node_set['geometry'].x,
            self.am.node_set['geometry'].y
        )
        self.am.node_set.drop_duplicates(subset=['Category', 'node_ids'], inplace=True)
        pass

    def calc_ga_node_ids(self):
        nodes_df, _ = self.st.get_current_nodes_and_edges()
        net = self.st.current_scenario['net']
        ga_idxs = self.ga.get_green_areas_ids()
        ga_nodes_set = []
        for idx in ga_idxs:
            points = pd.DataFrame(self.ga.get_countour_by_id(idx), columns=['x', 'y', 'key'])
            ga_nodes_ids = net.get_node_ids(points['x'], points['y'])
            ga_nodes = nodes_df[nodes_df['osmid'].isin(ga_nodes_ids)]
            ga_nodes['ID_AV'] = idx
            ga_nodes_set.append(ga_nodes)

        ga_nodes_set = pd.concat(ga_nodes_set)
        ga_nodes_set.drop_duplicates('osmid', inplace=True)
        ga_nodes_set.reset_index(inplace=True, drop=True)
        self.ga.node_set = ga_nodes_set
        pass
        
    ######################################################################
    #### Funciones para calculo de indicadores numericos
    ######################################################################

    def calc_sidewalk_kpis(self):
        self.numeric_kpis['SidewalkMaterial'] = self.sm.calculate_scoring()
        pass
        
    ######################################################################
    #### Funciones para calculo de densidades
    ######################################################################

    def _calc_population_by_unit(self):
        if self.select_unit == 'block':
            self.population_by_unit = self.bk.get_current_scenario().rename(columns={'q_residents': 'population'})
        else:
            block_population = self.bk.get_current_scenario().copy()
            block_population['block_area'] = block_population.area
            intersection = gpd.overlay(self.unit, block_population, how='intersection')
            intersection['intersection_area'] = intersection.area
            intersection['population'] = intersection['q_residents']*intersection['intersection_area']/intersection[f'block_area']
            # Calcula la población dentro de cada unidad espacial
            population_by_unit = intersection.groupby(f'{self.select_unit}_id')['population'].sum().reset_index()
            # population_by_unit['population'] = np.round(population_by_unit['population'])
            population_by_unit = pd.merge(population_by_unit, self.unit, on=[f'{self.select_unit}_id'], how='outer')
            ppl_cols = [f'{self.select_unit}_id', 'population']
            population_by_unit = gpd.GeoDataFrame(data=population_by_unit[ppl_cols], geometry=population_by_unit['geometry'])
            population_by_unit['population'].fillna(0, inplace=True)
            self.population_by_unit = population_by_unit
        pass

    def calc_population_density(self):
        self._calc_population_by_unit()
        population_density = self.population_by_unit.copy()
        population_density = pd.merge(population_density, self.unit, on=[f'{self.select_unit}_id'])
        population_density['density'] = population_density['population']/population_density['area']
        ppl_density_cols = [f'{self.select_unit}_id', 'population', 'density', 'geometry_x']
        population_density = population_density[ppl_density_cols]
        self.population_density = gpd.GeoDataFrame(data=population_density.drop(columns=['geometry_x']), geometry=population_density['geometry_x'])
        pass
    
    def calc_amenities_density(self):
        amenities = self.am.get_current_amenities().copy()

        join_result = gpd.sjoin(amenities, self.unit, how='inner', op='within')
        # count_by_unit = join_result.groupby(f'{select_unit}_id')['counter'].agg('sum').reset_index()
        count_by_unit = join_result.groupby(f'{self.select_unit}_id').size().reset_index(name='amenities_count')
        count_by_unit = pd.merge(count_by_unit, self.unit, on=[f'{self.select_unit}_id'], how='outer')
        count_by_unit['amenities_count'].fillna(0, inplace=True)
        count_cols = [f'{self.select_unit}_id', 'amenities_count', 'centroid', 'area']
        count_by_unit = gpd.GeoDataFrame(data=count_by_unit[count_cols], geometry=count_by_unit['geometry'])
        count_by_unit['density'] = count_by_unit['amenities_count']/count_by_unit['area']
        self.amenities_density = count_by_unit
        pass


    ######################################################################
    #### Funciones para calculo de diversidad
    ######################################################################

    def calc_land_uses_diversity(self):
        self.unit['area_unit'] = self.unit.area
        # Intersection between land_uses and units
        intersection = gpd.sjoin(self.unit, self.lu.get_current_land_uses(), how="inner", op="intersects")
        intersection['area'] = intersection.area

        # Filter intersection geodataframe by columns
        inter_cols = [f'{self.select_unit}_id', 'Uso', 'area', 'area_unit', 'area_predio']
        intersection = intersection[inter_cols]

        total_inter_area = intersection.groupby([f'{self.select_unit}_id'])['area'].agg('sum').reset_index().rename(columns={'area': 'inter_area'})
        intersection = pd.merge(intersection, total_inter_area, on=f'{self.select_unit}_id')
        intersection['property_percentage'] = intersection['area']/intersection['inter_area']
        intersection['information_per_property'] = -1*intersection['property_percentage']*np.log(intersection['property_percentage'])
        diversity = intersection.groupby(f'{self.select_unit}_id')['information_per_property'].agg('sum').reset_index()
        diversity_map = pd.merge(diversity, self.unit, on=f'{self.select_unit}_id')
        diversity_map.rename(columns={'information_per_property': 'diversity'}, inplace=True)
        self.lu_diversity = gpd.GeoDataFrame(data=diversity_map['diversity'], geometry=diversity_map['geometry'])
        self.unit.drop(columns=['area_unit'], inplace=True)
        pass

    ######################################################################
    #### Funciones para calculo de proximidades
    ######################################################################

    def calc_travel_time_to_amenities(self):
        results_df = []
        # Calcular el camino más corto desde cada centroide de teselado hasta todos los nodos de amenities
        for index, row in self.am.get_current_amenities().iterrows():
            # print(row['geometry'])
            # print(row)
            destination_node_id = self.st.current_scenario['net'].get_node_ids([row['geometry'].x], [row['geometry'].y])
            destination_node_id = list(destination_node_id)[0]

            sources = self.unit['node_ids']
            destinations = [destination_node_id]*len(self.unit['node_ids'])

            shortest_paths = self.st.current_scenario['net'].shortest_path_lengths(sources, destinations)
            results_df.append(
                pd.DataFrame.from_dict(
                    {
                        'source': sources,
                        'destination': destinations,
                        f'{self.select_unit}_id': self.unit[f'{self.select_unit}_id'],
                        'Category': [row['Category']]*len(self.unit['node_ids']),
                        'path_lengths': shortest_paths,
                    }
                )
            )
        
        results_df = pd.concat(results_df)
        # display(results_df)

        # Encuentra el valor mínimo para cada categoría de amenity
        unit_cat = [f'{self.select_unit}_id','Category']
        paths_output = results_df.groupby(unit_cat)['path_lengths'].min().reset_index()
        paths_output = pd.merge(paths_output, results_df, on=unit_cat+['path_lengths'])
        paths_output = pd.merge(paths_output, self.unit[[f'{self.select_unit}_id','geometry']], on=f'{self.select_unit}_id')
        # display(paths_output)

        columns = ['source', 'destination', 'path_lengths', 'Category', f'{self.select_unit}_id', 'geometry']
        self.gdf_am_paths = gpd.GeoDataFrame(data=paths_output.drop(columns=['geometry']), geometry=paths_output['geometry'])
        self.gdf_am_paths = self.gdf_am_paths[columns]

        self.gdf_am_paths['travel_time'] = self.gdf_am_paths['path_lengths'].apply(calcular_tiempo)
        pass

        
    def calc_travel_time_to_green_areas(self):
        source = self.unit[[f'{self.select_unit}_id', 'node_ids']]
        destination = self.ga.node_set[['ID_AV', 'osmid']]

        combinations = list(itertools.product(source.to_records(index=False), destination.to_records(index=False)))
        combinations_list = [list(item1) + list(item2) for item1, item2 in combinations]
        df_columns = ['hex_id', 'source', 'ID_AV', 'destination']
        df_combinations = pd.DataFrame(combinations_list, columns=df_columns)
        df_combinations['path_lengths'] = self.st.current_scenario['net'].shortest_path_lengths(
            df_combinations['source'],
            df_combinations['destination']
        )
        df_combinations['class'] = df_combinations['ID_AV'].str[:2]
        min_lenght_idx = df_combinations.groupby(['hex_id', 'class'])['path_lengths'].idxmin().reset_index()
        min_paths = df_combinations.loc[min_lenght_idx['path_lengths']]
        min_paths['travel_time'] = min_paths['path_lengths'].apply(calcular_tiempo)
        min_paths = pd.merge(min_paths, self.unit[[f'{self.select_unit}_id', 'geometry']], on=[f'{self.select_unit}_id'])
        self.gdf_ga_paths = gpd.GeoDataFrame(data=min_paths.drop(columns=['geometry']), geometry=min_paths['geometry'])
        # for idx in range(len(self.unit)):
        #     source = self.unit.loc[idx, 'node_ids']
        #     source = [source]*len(self.ga.node_set)
        #     destination = self.ga.node_set['osmid']
        #     paths = self.st.current_scenario['net'].shortest_path_lengths(source, self.ga.node_set['osmid'])
        #     paths_df = pd.DataFrame.from_dict({
        #         'source': source,
        #         'destination': destination,
        #         'path_lengths': paths
        #     })
        #     paths_df.sort_values(by=['path_lengths'], inplace=True)
        #     # display(paths_df)
        #     paths_df.reset_index(inplace=True, drop=True)
        #     paths_df = paths_df.head(1)
        #     paths_df['ID_AV'] = self.ga.node_set[self.ga.node_set['osmid'] == paths_df.loc[0,'destination']]['ID_AV'].values[0]
        #     paths_df[f'{self.select_unit}_id'] = self.unit.loc[idx, f'{self.select_unit}_id']
        #     paths_output.append(paths_df)

        # paths_output = pd.concat(paths_output)
        # paths_output.reset_index(inplace=True, drop=True)
        # paths_output = pd.merge(paths_output, self.unit, on=f'{self.select_unit}_id')

        # columns = ['source', 'destination', 'path_lengths', 'ID_AV', f'{self.select_unit}_id', 'geometry']
        # self.gdf_ga_paths = gpd.GeoDataFrame(data=paths_output.drop(columns=['geometry']), geometry=paths_output['geometry'])
        # self.gdf_ga_paths = self.gdf_ga_paths[columns]

        # self.gdf_ga_paths['travel_time'] = self.gdf_ga_paths['path_lengths'].apply(calcular_tiempo)
        pass

    ######################################################################
    #### Funciones GET
    ######################################################################

    def get_streets(self):
        return self.st if 'Streets' in self.modules_available else None
    
    def get_green_area(self):
        return self.ga if 'GreenAreas' in self.modules_available else None
    
    def get_amenities(self):
        return self.am if 'Amenities' in self.modules_available else None
    
    def get_travels_amenities(self):
        return self.gdf_am_paths
    
    def get_travels_green_areas(self):
        return self.gdf_ga_paths
    
    def get_amenities_categories(self):
        return self.am.get_categories()

    def get_travels_amenities_by_category(self, category):
        return self.gdf_am_paths[self.gdf_am_paths['Category']==category].drop(columns=['Category'])
    
    def get_travels_green_areas_by_class(self, green_area_class='PARQUE'):
        _class  = {'PARQUE': 'PK', 'PLAZA': 'SQ'}[green_area_class]
        return self.gdf_ga_paths[self.gdf_ga_paths['class']==_class].reset_index()
    
    def get_maps_green_areas(self):
        ret = {}
        for _class in ['PARQUE', 'PLAZA']:
            ret[_class] = self.get_travels_green_areas_by_class(_class)
        return ret

    ######################################################################
    #### Funciones de flujo de datos y archivos
    ######################################################################
    def save_heatmaps(self):
        self.save_amenities_travels()
        self.save_green_areas_travels()
        self.save_land_uses_diversity()
        pass

    def save_land_uses_diversity(self, path='/app/data/land_uses_diversity', zipped=True):
        
        scenario_name = self.dict_scenarios[self.present_scenario]
        scenario_path = f'{path}/{scenario_name}'
        verificar_y_crear_directorio(scenario_path)
        self.lu_diversity.to_file(scenario_path)

        if zipped:
            main = os.path.split(path)[-1]
            output_zip_path = f'/app/data/zip/{main}.zip'
            zip_folder(path, output_zip_path)
            
    def save_amenities_travels(self, path='/app/data/amenities_proximity', zipped=True):
        
        categories = self.get_amenities_categories()
        scenario_name = self.dict_scenarios[self.present_scenario]
        scenario_path = f'{path}/{scenario_name}'
        verificar_y_crear_directorio(scenario_path)
        for category in categories:
            filecat = category.lower().replace(' ','_')
            filename = f'{scenario_path}/{filecat}'
            self.get_travels_amenities_by_category(category).to_file(filename)

        if zipped:
            main = os.path.split(path)[-1]
            output_zip_path = f'/app/data/zip/{main}.zip'
            zip_folder(path, output_zip_path)
            
    def save_green_areas_travels(self, path='/app/data/green_areas_proximity', zipped=True):    
        
        scenario_name = self.dict_scenarios[self.present_scenario]
        scenario_path = f'{path}/{scenario_name}'
        verificar_y_crear_directorio(scenario_path)
        ga_travels = self.get_travels_green_areas()
        classes = list(ga_travels['class'].unique())
        [ga_travels[ga_travels['class']==_class].to_file(f'{scenario_path}_class') for _class in classes];
        
        if zipped:
            main = os.path.split(path)[-1]
            output_zip_path = f'/app/data/zip/{main}.zip'
            zip_folder(path, output_zip_path)