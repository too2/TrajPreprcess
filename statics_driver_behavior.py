import os
import pandas as pd
import geopandas as gpd
import vis_pre_traj
from objclass import TrajPoint, StayPoint
import utils

# Step0: 首先获取历史行程数最多的topK个司机（选择个数最多的那个司机）
# Step1: 对司机历史数据进行统计（看看平均统计值）
# Step2: 找到司机所属的停留点以及停留点的类型（看停留点）
# Step3: 分析在不同出发时段司机对停留点的偏好（不同出发时段有没有什么区别呢）
# Step4: 分析在不同终点司机对停留点的偏好（长短距离有什么影响呢）
# Step5: 找到看看是否存在相同的司机（偏好相同）（是否存在偏好相同的司机）
# 运单自身的信息

# Step0: (只保留出现次数大于一定值的司机)
his_traj = pd.read_csv('./data/relong_dist.csv')
df = his_traj.drop_duplicates(subset='waybill_no', keep='first')
df_new = df.groupby("dri_id").filter(lambda x: (len(x) >= 10))
print(df_new['dri_id'].value_counts())
new_traj = set(df_new['dri_id'].values)
traj_select_dri = his_traj[his_traj['dri_id'].isin(new_traj)]
traj_select_dri.to_csv('./data/step/traj_select_dri.csv', index=False)


# S1：
# 针对该司机轨迹数据进行预处理
# 去掉离起点和终点较远的轨迹点
# 首先判断开始的轨迹点离出发点的距离，直到小于一定阈值才保留，对于到达终点的情况，轨迹点距离终点一定距离后就进行截断

# 起点：日照钢厂（119.35426,35.15754）；终点：泰安钢材市场（117.06392,36.07603）
start_point = TrajPoint(None, None, 119.35426, 35.15754, None)
end_point = TrajPoint(None, None, 117.06392, 36.07603, None)

clean_traj_list = []
# 去掉起终点5公里范围内的停留点
for waybill_no, traj_data in traj_select_dri.groupby('waybill_no'):
    # 判断计算离起点还是离终点的情况
    tag_start = True
    for index, row in traj_data.iterrows():
        curr_point = TrajPoint(None, None, row['longitude'], row['latitude'], None)
        if tag_start:
            dist_start = utils.haversine_distance(start_point, curr_point)
            if dist_start > 2000:
                continue
            else:
                tag_start = False
                start_time = row['time']
        else:
            dist_end = utils.haversine_distance(end_point, curr_point)
            if dist_end < 2000:
                end_time = row['time']
                break
        clean_traj_list.append([row['plan_no'], row['waybill_no'], row['dri_id'], row['longitude'], row['latitude'], row['time']])

clean_traj = pd.DataFrame(data=clean_traj_list, columns=['plan_no', 'waybill_no', 'dri_id', 'longitude', 'latitude', 'time'])
clean_traj.to_csv('./data/clean_relong_dist.csv', index=False)
# 选择的top个司机
# U000049112    24
# U000092644    23
# U000104487    15
# U000118072    14
# 选择其中一个司机进行可视化 (U000049112, U000092644)

# 保存司机历史轨迹
dri_traj = clean_traj[clean_traj['dri_id'] == 'U000075382']
dri_traj.to_csv('./data/step/dri_traj_U000075382.csv', index=False)



