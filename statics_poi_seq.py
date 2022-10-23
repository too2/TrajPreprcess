import pandas as pd
import numpy as np
from collections import defaultdict
import os
from objclass import SPSeq, StayPoint
from datetime import datetime

# 每个停留点的数据
data = pd.read_csv('/Volumes/T7/traj_file/taian/merge_dri_sp_poi.csv')

# # 构造POI序列关系
# poi_dict = defaultdict(int)
# avg_data = 0
# for index, value in data.groupby('waybill_no'):
#     avg_data += len(value)
#     poi_seq = []
#     for index2, value2 in value.iterrows():
#         poi_seq.append(value2['poi_type'])
#     poi_dict['&'.join(poi_seq)] += 1
#     # print('&'.join(poi_seq))
# # print(poi_dict)
#
# df_tag = pd.read_csv('/Volumes/T7/traj_file/taian/cluster_result_stay_point_remove_od_dbscan_cluster_id.csv')
# # print(len(set(df_tag['cluster_id'])))
# print(len(set(df_tag['label'][df_tag['label'] >= 0])))
#
# a = sorted(poi_dict.items(), key=lambda x: x[1], reverse=True)
# print(a)
# print(avg_data)
# avg_data /= len(set(data['waybill_no']))
# print(avg_data)

# 统计不同出发时段，POI类别序列的影响
# 只是为了获取行程开始时间
path = '/Volumes/T7/traj_file/taian'
filename = 'new_traj_flow.csv'
traj_data = pd.read_csv(os.path.join(path, filename))
traj_data.drop_duplicates(subset='waybill_no', keep='first', inplace=True)
print(traj_data.head())

spseq_list = []
ans_waybill = 0
for waybill, seq in data.groupby('waybill_no'):
    plan_no = seq['plan_no'].values[0]
    waybill_no = seq['waybill_no'].values[0]
    dri_id = seq['dri_id'].values[0]
    start_time = traj_data[traj_data['waybill_no'] == waybill]['time'].values[0]
    start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    spseqobj = SPSeq(plan_no, waybill_no, dri_id, start_time)
    for index, sp in seq.iterrows():
        cen_lng = sp['longitude']
        cen_lat = sp['latitude']
        start_staytime = sp['start_stay']
        start_staytime = datetime.strptime(start_staytime, "%Y-%m-%d %H:%M:%S")
        duration = sp['duration']
        dist = sp['dist']
        spobj = StayPoint(cen_lng, cen_lat, start_staytime, duration, dist, waybill_no, plan_no, dri_id)
        spobj.type = sp['poi_type']
        spseqobj.sequence.append(spobj)
    spseq_list.append(spseqobj)
    ans_waybill += 1

# 划分时段、司机编号进行统计
split_time_seq = dict()
split_dri_id = dict()
split_time_dri_id = dict()
for seqobj in spseq_list:
    start_hour = seqobj.start_time.hour
    dri_id = seqobj.dri_id
    split_time_seq.setdefault(start_hour, []).append(seqobj)
    split_dri_id.setdefault(dri_id, []).append(seqobj)
    split_time_dri_id.setdefault(start_hour, {})
    split_time_dri_id[start_hour].setdefault(dri_id, []).append(seqobj)

print('==========')

for start_hour, value in split_time_dri_id.items():
    print("时刻：", start_hour, "停留序列个数：", len(split_time_seq[start_hour]))
    for dri_id, value2 in value.items():
        poi_dict = defaultdict(int)
        waybill_no = []
        plan_no = []
        print("司机ID", dri_id, ":")
        for seqobj in value2:
            # print(seqobj.get_seq_class())
            waybill_no.append(seqobj.waybill_no)
            plan_no.append(seqobj.plan_no)
            poi_dict['&'.join(seqobj.get_seq_class())] += 1
        print(waybill_no)
        print(plan_no)
        poi_dict = sorted(poi_dict.items(), key=lambda x: x[1], reverse=True)
        print(poi_dict)
        print(' ')


# for hour, seqobjlist in split_time_seq.items():
#     print("时刻：", hour, "停留序列个数：", len(seqobjlist))
#     poi_dict = defaultdict(int)
#     for seqobj in seqobjlist:
#         # print(seqobj.get_seq_class())
#         poi_dict['&'.join(seqobj.get_seq_class())] += 1
#     poi_dict = sorted(poi_dict.items(), key=lambda x: x[1], reverse=True)
#     print(poi_dict)
#     print()


# for dri_id, seqobjlist in split_dri_id.items():
#     print("司机：", dri_id, "停留序列个数：", len(seqobjlist))
#     poi_dict = defaultdict(int)
#     for seqobj in seqobjlist:
#         # print(seqobj.get_seq_class())
#         poi_dict['&'.join(seqobj.get_seq_class())] += 1
#     poi_dict = sorted(poi_dict.items(), key=lambda x: x[1], reverse=True)
#     print(poi_dict)
#     print()


