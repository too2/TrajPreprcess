import pandas as pd
import numpy as np
import os
# #
# filename = './data/step_new/staypoint_all.csv'
# traj_data = pd.read_csv(filename)
# #
# print(traj_data.columns)
# print(np.mean(traj_data.groupby(['plan_no'])['plan_no'].count()))
# print(len(traj_data.groupby(['plan_no'])['plan_no']))
# print(len(traj_data.groupby(['plan_no'])['plan_no'].filter(lambda x: len(x)<=3 and len(x)>=1)))

filename = './data/step_new/clean_relong_dist.csv'
traj_data = pd.read_csv(filename, nrows=10)
print(traj_data.head(10))
