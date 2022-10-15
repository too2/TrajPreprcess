import os
import pandas as pd
import geopandas as gpd

path = './data'
filename = 'stop_type.geojson'
file = open(os.path.join(path, filename))
gdf = gpd.read_file(file)
print(gdf.columns)




# traj_U000049112 = pd.read_csv('./data/step/dri_traj_U000049112.csv')
# traj_U000092644 = pd.read_csv('./data/step/dri_traj_U000092644.csv')


