import pandas as pd
from sklearn.cluster import DBSCAN
from objclass import StayPoint
import utils
from objclass import TrajPoint

# 求平均坐标
def calc_avg_loc(coors):
    sum_lng = 0
    sum_lat = 0
    for p in coors:
        sum_lng += p[0]
        sum_lat += p[1]
    return sum_lng / len(coors), sum_lat / len(coors)


def write2csv(ans, labels, save_path):
    sp_list = []
    for sp, label in zip(ans, labels):
        lng = sp.cen_lng
        lat = sp.cen_lat
        start = sp.start_staytime
        duration = sp.duration
        waybill_no = sp.waybill_no
        plan_no = sp.plan_no
        dri_id = sp.dri_id
        sp_list.append([plan_no, waybill_no, dri_id, lng, lat, start, duration, label])
    sp_df = pd.DataFrame(data=sp_list,
                         columns=['plan_no', 'waybill_no', 'dri_id', 'longitude', 'latitude', 'start_stay',
                                  'duration', 'label'])
    try:
        sp_df.to_csv(save_path, index=False)
    except Exception as e:
        print(e)


# DBSCAN聚类形成微簇
def do_DBSCAN_for_staypoints(spobj_list, eps=5, min_sample=5):
    cenpoi_list = [utils.wgs84_to_mercator(spobj.cen_lng, spobj.cen_lat) for spobj in spobj_list]
    labels = DBSCAN(eps=eps, min_samples=min_sample, metric='euclidean').fit(cenpoi_list).labels_
    for i in range(0, len(labels)):
        spobj_list[i].cluster_id = labels[i]
    return spobj_list, labels


if __name__ == '__main__':
    # 对停留点进行聚类
    sp_data_remove_od = pd.read_csv('./data/extract_sp.csv')
    spobj_list = []
    for index, row in sp_data_remove_od.iterrows():
        # 去掉起点10公里范围内，终点3公里范围内的停留点
        # 起点：日照钢厂（119.35426,35.15754）；终点：泰安钢材市场（117.06392,36.07603）
        start_point = TrajPoint(None, None, 119.35426, 35.15754, None)
        end_point = TrajPoint(None, None, 117.06392, 36.07603, None)
        curr_point = TrajPoint(None, None, row['longitude'], row['latitude'], None)
        dist_start = utils.haversine_distance(start_point, curr_point)
        dist_end = utils.haversine_distance(end_point, curr_point)
        if dist_start < 10000 or dist_end < 3000:
            continue
        spobj_list.append(StayPoint(plan_no=row['plan_no'], waybill_no=row['waybill_no'], dri_id=row['dri_id'],
                                    cen_lng=row['longitude'], cen_lat=row['latitude'],
                                    start_staytime=row['start_stay'], duration=row['duration']))
    miniclus, labels = do_DBSCAN_for_staypoints(spobj_list, eps=15, min_sample=2)
    write2csv(miniclus, labels, './data/cluster_result_stay_point_200m_12min_remove_od_dbscan.csv')

