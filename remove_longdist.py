import pandas as pd
import osmnx as ox
import os
import utils
from objclass import TrajPoint, Traj, TrajAll
from tqdm import tqdm
DIST_THRESHOLD = 1000

# 提取泰安市轨迹数据
path = '/Users/kxz/JupyterProjects/DASFAA'
filename = 'select_traj_taian.csv'
traj_data = pd.read_csv(os.path.join(path, filename))

# 将司机id赋予轨迹数据
# 运单匹配
waybill_data = pd.read_csv('/Volumes/新加卷/DASFAA/data/waybill_data_name.csv')

traj_all = TrajAll()
for waybill_no, data in traj_data.groupby('waybill_no'):
    dri_id = waybill_data[waybill_data['waybill_no'] == waybill_no]['driver_id'].values[0]
    trajectory = Traj(list(data['plan_no'])[0], waybill_no, dri_id)
    traj_all.traj_dict[waybill_no] = trajectory
    point_list = []
    for index, traj in data.iterrows():
        point = TrajPoint(traj['plan_no'], traj['waybill_no'], traj['longitude'], traj['latitude'], traj['time'])
        point_list.append(point)
    trajectory.traj_point_list = point_list

# 轨迹去噪，清除轨迹中轨迹点间距较大的轨迹
save_traj = []
for waybill_no, traj_obj in tqdm(traj_all.traj_dict.items()):
    flag = False
    for index, traj_point_obj in enumerate(traj_obj.traj_point_list):
        if index == 0:
            curr_point = traj_point_obj
            last_point = curr_point
        else:
            curr_point = traj_point_obj
            dist = utils.haversine_distance(curr_point, last_point)
            if dist > DIST_THRESHOLD:
                flag = True
                break
            last_point = curr_point
    if not flag:
        save_traj.append(traj_obj)

print(len(save_traj))


save_data = []
for traj in tqdm(save_traj):
    plan_no = traj.plan_no
    waybill_no = traj.waybill_no
    dri_id = traj.dri_id
    traj_list = traj.traj_point_list
    for point in traj_list:
        longitude = point.longitude
        latitude = point.latitude
        timestamp = point.time
        save_data.append([plan_no, waybill_no, dri_id, longitude, latitude, timestamp])

df_save = pd.DataFrame(data=save_data, columns=['plan_no', 'waybill_no', 'dri_id', 'longitude', 'latitude', 'time'])
df_save.to_csv('./data/relong_dist.csv', index=False)
