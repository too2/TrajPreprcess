import os
import pandas as pd
import geopandas as gpd
import vis_pre_traj
import utils
from tqdm import tqdm

filename = 'clean_relong_dist.csv'
save_name = 'U000070691'
save_path = './data/step_new'
path = './data/step_new'
data = pd.read_csv(os.path.join(path, filename))
data['time'] = pd.to_datetime(data['time'], format='%Y-%m-%d %H:%M:%S')

# 是否只选择一条轨迹可视化
plot_traj = data[data['dri_id'] == 'U000070691']
i = 0
for plan_no, value in plot_traj.groupby(['plan_no']):
    print(i, plan_no, value['time'].values[0])
    i += 1
