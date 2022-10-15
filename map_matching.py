import pandas as pd
import numpy as np
import osmnx as ox
import time
from tqdm import tqdm
from leuvenmapmatching.matcher.distance import DistanceMatcher
from leuvenmapmatching.map.inmem import InMemMap
from leuvenmapmatching import visualization as mmviz
from multiprocessing.pool import Pool
import geopandas as gpd
import os
import warnings

warnings.filterwarnings("ignore")

t1 = time.time()
print(1)


# 获取山东省路网
# shandong = ox.graph.graph_from_place('shandong', network_type='drive')
# ox.io.save_graphml(shandong, 'shandong.graphml')
G_polygon = ox.io.load_graphml('/Users/kxz/JupyterProjects/DASFAA/shandong.graphml')

nodes, edges = ox.utils_graph.graph_to_gdfs(G_polygon)
edges['lon'] = edges.centroid.x
edges['lat'] = edges.centroid.y
# 转换路网的坐标系
G_p = ox.project_graph(G_polygon, to_crs=2416)
nodes_p, edges_p = ox.graph_to_gdfs(G_p, nodes=True, edges=True)

# 将路网转换为网络
map_con = InMemMap(name='pNEUMA', use_latlon=False)  # , use_rtree=True, index_edges=True)

# 构建网络
for node_id, row in nodes_p.iterrows():
    map_con.add_node(node_id, (row['y'], row['x']))
for node_id_1, node_id_2, _ in G_p.edges:
    map_con.add_edge(node_id_1, node_id_2)

# 读取轨迹数据
filename = 'clean_relong_dist.csv'
path = '/Users/kxz/PycharmProjects/TrajPreprocess/data/step_new/'
data = pd.read_csv(os.path.join(path, filename))
data = data[data['dri_id'] == 'U000070691']

#转换轨迹的坐标系为地理坐标系
data['geometry'] = gpd.points_from_xy(data['longitude'], data['latitude'])
data = gpd.GeoDataFrame(data)
data.crs = {'init': 'epsg:4326'}
data = data.to_crs(2416)

print(len(set(data['plan_no'])))
t2 = time.time()
print(t2-t1, 's')


# 构建地图匹配工具
matcher = DistanceMatcher(map_con,
                          max_dist=3000,
                          max_dist_init=2000,
                          min_prob_norm=0.0001,
                          non_emitting_length_factor=0.95,
                          obs_noise=500,
                          obs_noise_ne=500,
                          dist_noise=500,
                          max_lattice_width=200,
                          non_emitting_states=True)


def do_mm(param):
    plan_no = param[0]
    path = param[1]
    mm_result = {}
    # 进行地图匹配
    states, _ = matcher.match(path, unique=False)
    mm_result[plan_no] = states
    # print(states)
    return mm_result


if __name__ == '__main__':
    param_list = []
    for plan_no, pre_path in tqdm(data.groupby('plan_no')):
        # 获得轨迹点
        path = list(zip(pre_path.geometry.y, pre_path.geometry.x))
        param_list.append((plan_no, path))
    t1 = time.time()
    with Pool(2) as pool:
        progress_bar = tqdm(total=len(param_list))
        res = list(tqdm(pool.imap(do_mm, param_list), total=len(param_list)))
    # res = pool.map(do_mm, param_list)
    # print('-------------')
    # print(res)
    # print('--------------')
    res = np.array(res)
    np.save('./data/step_new/res.npy', res)
    t2 = time.time()
    print("并行执行时间：{}s".format(int(t2 - t1)))

