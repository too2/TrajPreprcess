import pandas as pd
import utils
from objclass import TrajPoint, Traj, TrajAll
from tqdm import tqdm

# Step0: 首先获取历史行程数最多的topK个司机（选择个数最多的那个司机）
# Step1: 对司机历史数据进行统计（看看平均统计值）
# Step2: 找到司机所属的停留点以及停留点的类型（看停留点）
# Step3: 分析在不同出发时段司机对停留点的偏好（不同出发时段有没有什么区别呢）
# Step4: 分析在不同终点司机对停留点的偏好（长短距离有什么影响呢）
# Step5: 找到看看是否存在相同的司机（偏好相同）（是否存在偏好相同的司机）
# 运单自身的信息

'''
# Step0: (只保留出现次数大于一定值的司机)
his_traj = pd.read_csv('./data/step_new/traj_taian.csv')
df = his_traj.drop_duplicates(subset='waybill_no', keep='first')
df_new = df.groupby("dri_id").filter(lambda x: (len(x) >= 10))
print(df_new['dri_id'].value_counts())
new_traj = set(df_new['dri_id'].values)
traj_select_dri = his_traj[his_traj['dri_id'].isin(new_traj)]
traj_select_dri.to_csv('./data/step_new/traj_select_dri.csv', index=False)
'''
traj_select_dri = pd.read_csv('./data/step_new/traj_select_dri.csv')

traj_all = TrajAll()
for waybill_no, data in traj_select_dri.groupby('waybill_no'):
    dri_id = data['dri_id'].values[0]
    trajectory = Traj(list(data['plan_no'])[0], waybill_no, dri_id)
    traj_all.traj_dict[waybill_no] = trajectory
    point_list = []

    last_time = None
    for index, traj in enumerate(data.itertuples()):
        if index == 0:
            pass
        else:
            if last_time == traj.time:
                last_time = traj.time
                continue
        point = TrajPoint(traj.plan_no, traj.waybill_no, traj.longitude, traj.latitude, traj.time)
        last_time = traj.time
        point_list.append(point)
    trajectory.traj_point_list = point_list

# 计算轨迹点距离起点已行驶的距离
last_point = None
for waybill_no, traj_obj in tqdm(traj_all.traj_dict.items()):
    for index, traj_point_obj in enumerate(traj_obj.traj_point_list):
        if index == 0:
            curr_point = traj_point_obj
            last_point = curr_point
            traj_point_obj.dist = 0
        else:
            curr_point = traj_point_obj
            dist = utils.haversine_distance(curr_point, last_point)
            curr_point.dist = last_point.dist + dist
            last_point = curr_point

save_data = []
for waybill_no, traj_obj in tqdm(traj_all.traj_dict.items()):
    plan_no = traj_obj.plan_no
    dri_id = traj_obj.dri_id
    traj_list = traj_obj.traj_point_list
    for point in traj_list:
        longitude = point.longitude
        latitude = point.latitude
        timestamp = point.time
        dist = point.dist
        save_data.append([plan_no, waybill_no, dri_id, longitude, latitude, timestamp, dist])

df_save = pd.DataFrame(data=save_data, columns=['plan_no', 'waybill_no', 'dri_id', 'longitude', 'latitude', 'time', 'dist'])
# 计算每个轨迹点离起点开始行驶的距离（方便后续计算距离）只是这里名为clean_relong_dist
df_save.to_csv('./data/step_new/clean_relong_dist.csv', index=False)


# 保存司机历史轨迹
# dri_traj = clean_traj[clean_traj['dri_id'] == 'U000075382']
# dri_traj.to_csv('./data/step/dri_traj_U000075382.csv', index=False)



