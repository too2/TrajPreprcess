import pandas as pd
import os
import geopandas as gpd
import objclass
import numpy as np
from shapely.geometry import Polygon, Point
import utils_poi
from requests_html import HTMLSession
import json
from tqdm import tqdm

'''
# 先前代码，现在不用人工标注了
# 完成S2
dri_traj_U000049112 = pd.read_csv('./data/step/dri_traj_U000049112.csv')
dri_traj_U000092644 = pd.read_csv('./data/step/dri_traj_U000092644.csv')
dri_traj_U000049112 = dri_traj_U000049112.drop_duplicates(subset='waybill_no', keep='first')
print(dri_traj_U000049112['time'])

dri_traj_U000092644 = dri_traj_U000092644.drop_duplicates(subset='waybill_no', keep='first')
print(dri_traj_U000092644['time'])

# 读取标注停留热点区域
path = './data'
filename = 'stop_type.geojson'
file = open(os.path.join(path, filename))
gdf = gpd.read_file(file)
print(gdf.columns)

stay_area = []
for index, value in gdf.iterrows():
    sr = objclass.StayRegion(index)
    if value['rest']:
        sr.type = 'rest'
    elif value['gas']:
        sr.type = 'gas'
    else:
        sr.type = 'space'
    sr.polygon = value['geometry']
    stay_area.append(sr)

def is_tag_area(stay_area, sp):
    """
    判断停留点是否落在标注区域内
    :param stay_area: 停留区域
    :param sp: 停留点
    :return:
    """
    x, y = sp[0], sp[1]
    p = Point(x, y)
    for sr in stay_area:
        if sr.polygon.contains(p):
            return True
    return False


# 对单条轨迹的停留点检测
# 首先读取所有停留点属性，并查看每条轨迹有多少轨迹点落在这个停留点上
# （发现司机对于停留点属性序列的偏好性）
extract_sp = pd.read_csv('./data/extract_sp.csv')
num_sp = []
avg_sp = []
for waybill_no, value in dri_traj_U000049112.groupby('waybill_no'):
    sp_data = extract_sp[extract_sp['waybill_no'] == waybill_no]
    sp_get = 0
    for index, value in sp_data.iterrows():
        if is_tag_area(stay_area, (value['longitude'], value['latitude'])):
            sp_get += 1
    num_sp.append(sp_get/len(sp_data))
    avg_sp.append(len(sp_data))
print(np.average(num_sp))
print(np.average(avg_sp))
'''

# # 一共有多少停留点 696
# extract_sp = pd.read_csv('./data/extract_sp.csv')
# print(len(extract_sp))

# 给每个簇打上label
data = pd.read_csv('/Volumes/T7/traj_file/taian/cluster_result_stay_point_remove_od_dbscan.csv')
print(data.head(1))
label2id = []
num_nega = 0
for index, value in data.iterrows():
    if value['label'] == -1:
        label2id.append(str(num_nega)+'_-1')
        num_nega += 1
    else:
        label2id.append(str(value['label']))
label2id = pd.DataFrame(data=label2id, columns=['cluster_id'])
data = pd.concat([data, label2id], axis=1)

data.to_csv('/Volumes/T7/traj_file/taian/cluster_result_stay_point_remove_od_dbscan_cluster_id.csv', index=False)


# 一共有多少行程中停留点 150
cluster_sp_data = pd.read_csv('/Volumes/T7/traj_file/taian/cluster_result_stay_point_remove_od_dbscan_cluster_id.csv')
print(cluster_sp_data.head(1))
label_1 = cluster_sp_data[cluster_sp_data['label'] == -1]
label_other = cluster_sp_data[cluster_sp_data['label'] != -1]
label_other = label_other.drop_duplicates(subset='label', keep='first')
label_all = pd.concat([label_1, label_other])

# 查找每个停留点对应的POI
label_all['location_gcj'] = label_all.apply(utils_poi.wgs84togaode_arr, axis=1,
                                            args=('longitude', 'latitude'))

def get_poi(radius: int, data, keys: list):
    ans = {}
    radius_list = [radius]
    keys_index = 0
    for index, center_point in tqdm(data.iterrows()):
        if index % 1500 == 0 and index != 0:
            keys_index += 1
        for num in radius_list:
            PoiTypes = ['010100', '050000', '180300']
            key = keys[keys_index]
            for PoiType in PoiTypes:
                params = {
                    "key": key,
                    "location": [str(round(getattr(center_point, 'location_gcj')[0], 6))+','+\
                                 str(round(getattr(center_point, 'location_gcj')[1], 6))],
                    "types": PoiType,
                    "radius": num,
                    "output": "json",
                }
                url = 'https://restapi.amap.com/v3/place/around'
                session = HTMLSession()
                try:
                    rq = session.get(url, params=params)
                    result = json.loads(rq.html.html)
                    # 控制时间反爬虫
                    # time.sleep(random.randint(3, 4))
                    total_page = result['count']
                    ans.setdefault(str(PoiType) + '_' + str(num), []).append(total_page)
                except:
                    keys_index += 1
                    key = keys[keys_index]
                    rq = session.get(url, params=params)
                    result = json.loads(rq.html.html)
                    # 控制时间反爬虫
                    # time.sleep(random.randint(3, 4))
                    total_page = result['count']
                    ans.setdefault(str(PoiType) + '_' + str(num), []).append(total_page)
            cluster_id = str(getattr(center_point, 'cluster_id'))
            ans.setdefault('cluster_id', []).append(cluster_id)
    ans = pd.DataFrame(ans)
    return ans

# 高德接口
keys = ['64584c960e74016089037d213a11b650', '6a4d78871c3aac0f548c0bc2e4784546','db188494399ade7fa94919034ef83e5c',\
        'e148068c41fecb7585a8c19f6f2cb65e','792bb14354d3624305d64d7f0d2d9c34']
data = label_all[['location_gcj', 'cluster_id']]
radius = 150
ans = get_poi(radius, data, keys)

PoiTypes = ['010100', '050000', '180300']
names = ['汽车服务_加油站', '餐饮服务', '道路附属设施_服务区']
radius_all = [150]
columns = {}
for r in radius_all:
    for name, PoiType in zip(names, PoiTypes):
        columns[PoiType+'_'+str(r)] = name+'_'+str(r)

ans.rename(columns=columns, inplace=True)
print(ans.head())
ans.to_csv('/Volumes/T7/traj_file/taian/sp_poi.csv', index=False)

