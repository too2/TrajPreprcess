import os
import pandas as pd
from tqdm import tqdm

# traj_data = pd.read_csv('/Volumes/T7/traj_file/taian/new_traj_flow.csv')
# save_path = '/Volumes/T7/traj_file/taian/traj_cleaning/'
# for waybill_no, value in tqdm(traj_data.groupby('waybill_no')):
#     filename = str(waybill_no) + '.csv'
#     value.to_csv(os.path.join(save_path, filename), index=False)

save_path = '/Volumes/T7/traj_file/taian/traj_cleaning/'
print(len(os.listdir(save_path)))
