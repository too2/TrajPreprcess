import pandas as pd

#
his_traj = pd.read_csv('./data/relong_dist.csv')
df = his_traj.drop_duplicates(subset='waybill_no', keep='first')

#
