import pandas as pd

# 可视化停留点信息
data = pd.read_csv('/Volumes/T7/traj_file/taian/merge_dri_sp_poi.csv')
# save_way = ('YD201113000084', 'YD201122000247')
# save_data = data[data['waybill_no'].isin(save_way)]
save_data = data[data['dri_id'] == 'U000001351']
save_data.to_csv('/Volumes/T7/traj_file/taian/U000001351_sp.csv', index=False)

# 可视化轨迹数据
traj_data = pd.read_csv('/Volumes/T7/traj_file/taian/new_traj_flow.csv')
save_traj_data = traj_data[traj_data['dri_id'] == 'U000001351']
save_traj_data.to_csv('/Volumes/T7/traj_file/taian/U000001351_traj.csv', index=False)
