import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt
import datetime

pd.set_option('display.max_columns', None)

'''
cluster_id = 0
# 给每个簇打上label
data = pd.read_csv('./data/cluster_result_stay_point_200m_12min_remove_od_dbscan_cluster_id.csv')
sp_poi = pd.read_csv('./data/step/sp_poi.csv')

data = pd.merge(data, sp_poi, how='left', on='cluster_id')
data.to_csv('./data/step/dri_sp_poi.csv', index=False)
'''

data = pd.read_csv('./data/step/dri_sp_poi.csv')
# 选择一个司机，构造表，历史行程中，每个司机的POI值
print(len(set(data['dri_id'].values.tolist())))
print(len(set(data['waybill_no'].values.tolist())))
for dri_id, value in data.groupby('dri_id'):
    print(sum(value['汽车服务_加油站_150'].values.tolist()),
          sum(value['餐饮服务_150'].values.tolist()),
          sum(value['道路附属设施_服务区_150'].values.tolist()),
          dri_id)

# 没有加油行为 U000068559
# 有加油行为 U000075382

# 历史行程数最多的两个司机
# U000049112
# U000092644

# 获取上述两个司机每次行程的POI序列
# 格式：POI类型，开始停留时间，停留时长
# 统计两个司机每天的行程数目 (这里需要获取运单表信息)
# his_traj = pd.read_csv('./data/relong_dist.csv')
# df = his_traj.drop_duplicates(subset='waybill_no', keep='first')
#
# # print(df[df['plan_no'] == 'DD210103000401']['time'])
#
# trip_date_d1 = defaultdict(int)
# poi_U000049112 = data[data['dri_id'] == 'U000049112']
# for index, value in poi_U000049112.groupby('waybill_no'):
#
#     t = df[df['waybill_no'] == index]['time'].values[0]
#     trip_date_d1[t[:10]] += 1
#
# print(trip_date_d1)


# # 统计司机停留时长分布
# stay_time = []
# poi_U000049112 = data[data['dri_id'] == 'U000092644']
# for index, value in poi_U000049112.groupby('waybill_no'):
#     for v in value['duration'].values:
#         minutes = datetime.datetime.strptime(v[-8:], "%H:%M:%S")
#         stay_time.append(minutes.hour*60 + minutes.minute)
# # plt.xlabel('停留时长（分钟）')
# # plt.ylabel('停留次数（次）')
# plt.hist(stay_time)
# plt.show()

# 统计每次行程中停留点个数
# poi_U000092644 = data[data['dri_id'] == 'U000068559']
# num_stay = []
# for index, value in poi_U000092644.groupby('waybill_no'):
#     num_stay.append(len(value['duration'].values))
# print(num_stay)
# plt.hist(num_stay)
# plt.show()


# # 统计司机停留POI类型分布（根据一个规则去筛选哪些有餐馆的地区大概率是休息区）
# poi_U000092644 = data[data['dri_id'] == 'U000068559']
# space = 0
# rest = 0
# gas = 0
# for index, value in poi_U000092644.groupby('waybill_no'):
#     for index2, value2 in value.iterrows():
#         if value2['汽车服务_加油站_150'] > 0:
#             gas += 1
#         elif value2['餐饮服务_150'] > 0 and \
#                 ('18:30:00' < value2['start_stay'][-8:] < '19:30:00' or
#                  '06:30:00' < value2['start_stay'][-8:] < '08:30:00' or
#                  '11:30:00' < value2['start_stay'][-8:] < '12:30:00'):
#             rest += 1
#         else:
#             space += 1
# print(space, rest, gas)
# # 统计司机在不同出发时段（POI类型序列的变化关系）
poi_U000092644 = data[data['dri_id'] == 'U000092644']
poi_seq = []
poi_list = defaultdict(int)
for index, value in poi_U000092644.groupby('waybill_no'):
    for index2, value2 in value.iterrows():
        if value2['汽车服务_加油站_150'] > 0:
            poi_type = 'gas'
        elif value2['餐饮服务_150'] > 0 and \
                ('18:30:00' < value2['start_stay'][-8:] < '19:30:00' or
                 '06:30:00' < value2['start_stay'][-8:] < '08:30:00' or
                 '11:30:00' < value2['start_stay'][-8:] < '12:30:00'):
            poi_type = 'restaurant'
        else:
            poi_type = 'rest_area'
        poi_seq.append(poi_type)
    poi_list['&'.join(poi_seq)] += 1
print(poi_list)
