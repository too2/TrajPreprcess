import numpy as np
import pandas as pd
import os
from datetime import datetime

# mm_data = np.load(os.path.join(os.getcwd(), './data/step_new/res.npy'), allow_pickle=True)
# # print(mm_data)
#
# d1 = {}
# for i in mm_data:
#     d1.update(i)
#
# up_road = []
# down_road = []
#
# new_mm = []
# for mm in mm_data:
#     value = list(mm.values())[0]
#     key = list(mm.keys())[0]
#     flag = True
#     tmp = []
#     [tmp.append(i) for i in value if i not in tmp]
#     for node in tmp:
#         if node == (6537160123, 7771618037):
#             down_road.append({key: tmp})
#             flag = False
#             break
#     if flag:
#         up_road.append({key: tmp})
#
# '''
# # 分析两条道路不同的原因
# # 1、首先获取出发时段
# # 2、获取旅行时长
# # 3、获取行驶距离
# # 4、查看有没有停留行为
# # 5、与油耗最短、距离最短等方法进行比较
# '''
#
# traj = pd.read_csv('/Volumes/T7/clean_relong_dist.csv')
# traj_dri = traj[traj['dri_id'] == 'U000070691']
# # for plan_no, value in traj_dri.groupby('plan_no'):
# #     print(plan_no, len(value))
# #     print(len(d1[plan_no]))
# #     print("=========================")
# print(len(set(traj_dri['plan_no'].values)))
#
# for i in up_road:
#     print(i.keys())
# print('=====================')
# for j in down_road:
#     print(j.keys())


dri_traj = pd.read_excel('/Volumes/T7/分析司机为什么走不同的路.xlsx')
print(dri_traj.head())
down_t = []
up_t = []

down_start = []
up_start = []

down_dist = []
up_dist = []

for index, value in enumerate(dri_traj.itertuples()):
    t0 = datetime.strptime(value.start_date, '%Y-%m-%dT%H:%M:%S.000')
    t1 = datetime.strptime(value.end_date, '%Y-%m-%dT%H:%M:%S.000')
    d0 = value.start_dist
    d1 = value.end_dist
    if index < 4:
        up_t.append((t1-t0).total_seconds()/60)
        up_start.append(t0.strftime("%m/%d/%Y, %H:%M:%S"))
        up_dist.append(d1-d0)
    else:
        down_t.append((t1-t0).total_seconds()/60)
        down_start.append(t0.strftime("%m/%d/%Y, %H:%M:%S"))
        down_dist.append(d1-d0)

print(up_t)
print(down_t)
print(np.mean(up_t))
print(np.mean(down_t))
print('=======')
print(up_start)
print(down_start)
print('=======')
print(up_dist)
print(down_dist)
up_dist[1] = up_dist[0]
print(np.mean(up_dist))
print(np.mean(down_dist))
print(np.mean(down_dist)-np.mean(up_dist))

# 1、看有没有限行区域
# 2、看道路等级的影响
# 3、弄清mm
