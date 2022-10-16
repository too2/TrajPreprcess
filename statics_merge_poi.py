import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt
import datetime
import os

# 1、读取文件
pd.set_option('display.max_columns', None)
if os.path.exists('/Volumes/T7/traj_file/taian/dri_sp_poi.csv'):
    # 给每个簇打上label
    data = pd.read_csv('/Volumes/T7/traj_file/taian/cluster_result_stay_point_remove_od_dbscan_cluster_id.csv')
    sp_poi = pd.read_csv('/Volumes/T7/traj_file/taian/sp_poi.csv')
    data = pd.merge(data, sp_poi, how='left', on='cluster_id')
    data.to_csv('/Volumes/T7/traj_file/taian/dri_sp_poi.csv', index=False)
else:
    data = pd.read_csv('/Volumes/T7/traj_file/taian/dri_sp_poi.csv')


def get_time(row):
    return datetime.datetime.strptime(row['start_stay'], '%Y-%m-%d %H:%M:%S')

def get_duration_seconds(row):
    c = row['duration']
    c = c.split(' ')
    t = int(c[0]) * 24 * 3600
    tmp = c[-1].split(':')
    t += int(tmp[0]) * 3600
    t += int(tmp[1]) * 60
    t += int(tmp[2])
    return t

def judge_type(value):
    if value['汽车服务_加油站_150'] > 0 and value['duration_seconds'] < 40 * 60:
        poi_type = 'gas'
    elif value['餐饮服务_150'] > 0 and \
            ('18:30:00' < value['start_stay'][-8:] < '19:30:00' or
             '06:30:00' < value['start_stay'][-8:] < '08:30:00' or
             '11:30:00' < value['start_stay'][-8:] < '12:30:00'):
        poi_type = 'restaurant'
    else:
        poi_type = 'rest_area'
    return poi_type

data['new_start_stay'] = data.apply(lambda x: get_time(x), axis=1)
data['duration_seconds'] = data.apply(lambda x: get_duration_seconds(x), axis=1)
data['poi_type'] = data.apply(lambda x: judge_type(x), axis=1)

# 2、合并距离相近，时间相近的停留点
dri_sp_poi_merge = []
for index, value in data.groupby('waybill_no'):
    anchor = None
    value = value.reset_index(drop=True)
    for index2, curr in value.iterrows():
        if index2 == 0:
            anchor = curr
            continue
        else:
            t = (curr['new_start_stay'] - anchor['new_start_stay']).total_seconds() - \
                anchor['duration_seconds']
            d = curr['dist'] - anchor['dist']
            if t < 10 * 60 and d < 10000:
                anchor['duration_seconds'] = (curr['new_start_stay'] - anchor['new_start_stay']).total_seconds() + \
                                             curr['duration_seconds']
                anchor['dist'] = (anchor['dist'] + curr['dist']) / 2
                if anchor['poi_type'] == 'gas' or curr['poi_type'] == 'gas':
                    anchor['poi_type'] = 'gas'
                elif anchor['poi_type'] == 'restaurant' or curr['poi_type'] == 'restaurant':
                    anchor['poi_type'] = 'restaurant'
                else:
                    anchor['poi_type'] = 'rest_area'
            else:
                dri_sp_poi_merge.append([anchor['plan_no'], anchor['waybill_no'], anchor['dri_id'],
                                         anchor['longitude'], anchor['latitude'], anchor['new_start_stay'],
                                         anchor['duration'], anchor['dist'], anchor['poi_type']])
                anchor = curr
    dri_sp_poi_merge.append([anchor['plan_no'], anchor['waybill_no'], anchor['dri_id'],
                             anchor['longitude'], anchor['latitude'], anchor['start_stay'],
                             anchor['duration'], anchor['dist'], anchor['poi_type']])

df = pd.DataFrame(data=dri_sp_poi_merge, columns=['plan_no', 'waybill_no', 'dri_id', 'longitude', 'latitude',
                                                  'start_stay', 'duration', 'dist', 'poi_type'])

df.to_csv('/Volumes/T7/traj_file/taian/merge_dri_sp_poi.csv', index=False)

print(df.head())

# 3、停留点标签赋值



# 构造POI序列关系
# poi_list = defaultdict(int)
# for index, value in data.groupby('waybill_no'):
#     poi_seq = []
#     for index2, value2 in value.iterrows():
#         if value2['汽车服务_加油站_150'] > 0:
#             poi_type = 'gas'
#         elif value2['餐饮服务_150'] > 0 and \
#                 ('18:30:00' < value2['start_stay'][-8:] < '19:30:00' or
#                  '06:30:00' < value2['start_stay'][-8:] < '08:30:00' or
#                  '11:30:00' < value2['start_stay'][-8:] < '12:30:00'):
#             poi_type = 'restaurant'
#         else:
#             poi_type = 'rest_area'
#         poi_seq.append(poi_type)
#     poi_list['&'.join(poi_seq)] += 1
#     print('&'.join(poi_seq))
# print(poi_list)



    


"""
# 选择一个司机，构造表，历史行程中，每个司机的POI值
# print(len(set(data['dri_id'].values.tolist())))
# print(len(set(data['waybill_no'].values.tolist())))
# for dri_id, value in data.groupby('dri_id'):
#     print(sum(value['汽车服务_加油站_150'].values.tolist()),
#           sum(value['餐饮服务_150'].values.tolist()),
#           sum(value['道路附属设施_服务区_150'].values.tolist()),
#           dri_id)

# 获得所有匹配数据，可视化，进行停留点挖掘，POI标注
# 想要提取的文件类型：每个历史行程对应POI序列，具体时间，间隔，看统计值能否发现规律
# 这里目前只能去找类别的关系，或者出发时段的关系，起终点的关系
# 开始复现STRNN


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
"""
