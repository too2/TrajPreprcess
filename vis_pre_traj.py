import json
import os
import pandas as pd


def visual_result(traj, path, save_path, type_style="MultiLineString"):
    """
    Args:
        list traj
        String path
        String type_style(Multipoint, LineString, Point)
    Returns:
        .json
    """
    dir_path = os.getcwd()
    save_path = os.path.join(dir_path, save_path, path)
    if os.path.exists(save_path):
        os.remove(save_path)
    with open(save_path, "w") as f:
        json.dump(geo_json_generate(traj, type_style), f)

def geo_json_generate(link_wkts, type_style="LineString"):
    res = {
        "type": "FeatureCollection",
        "features": []
    }
    for i, item in enumerate(link_wkts):
        for j in range(len(item[0])):
            t = {
                "type": "Feature",
                "geometry": {
                    "type": type_style, "coordinates": [item[0][j]]
                },
                "properties": {
                    # 'id': i,
                    # "waybill_no": item[2],
                    # 'truck_no': item[3],
                    'time': item[2][j],
                    'waybill_no': item[1],
                    'dri_id': item[3],
                    # 'end_point': item[4],
                }
            }
            res["features"].append(t)
    return res

def vis_trajs(traj_df, filename, save_path, mode='Multipoint'):
    data_list = traj_df.groupby(['waybill_no'])
    traj_list = []
    for waybill_no, traj in data_list:
        coors = traj[['longitude', 'latitude']].values.tolist()
        time = traj['time'].values.tolist()
        dri_id = traj['dri_id'].values.tolist()[0]
        # end_point = traj['end_point'].values.tolist()[0]
        traj_list.append([coors, waybill_no, time, dri_id])
    visfilename_point = f"{filename}_point.json"
    visfilename_line = f"{filename}_line.json"
    if mode == 'Multipoint':
        visual_result(traj_list, visfilename_point, save_path, 'Multipoint')
    else:
        visual_result(traj_list, visfilename_line, save_path, 'LineString')


def plot_traj(filename, save_name, path, dri_id=None):
    data_plot = pd.read_csv(os.path.join(path, filename))
    # data['time'] = pd.to_datetime(data['time'], format='%Y-%m-%d %H:%M:%S')

    # 是否只选择一条轨迹可视化
    if dri_id:
        data_plot = data_plot[data_plot['dri_id'] == dri_id]

    # 时间过滤
    # data = data[data['time'].dt.month.isin(np.arange(6, 7)) & data['time'].dt.year.isin([2021]) &
    #             data['time'].dt.day.isin(np.arange(1, 4))]
    vis_trajs(data_plot, save_name, save_path=path, mode='Multipoint')


if __name__ == "__main__":
    filename = 'relong_dist.csv'
    save_name = 'U000049112'
    path = './data'
    data = pd.read_csv(os.path.join(path, filename))
    # data['time'] = pd.to_datetime(data['time'], format='%Y-%m-%d %H:%M:%S')

    # 是否只选择一条轨迹可视化
    plot_traj = data[data['dri_id'] == 'U000049112']
    data = plot_traj

    # 时间过滤
    # data = data[data['time'].dt.month.isin(np.arange(6, 7)) & data['time'].dt.year.isin([2021]) &
    #             data['time'].dt.day.isin(np.arange(1, 4))]
    print(data.columns)

    vis_trajs(data, save_name, mode='Multipoint')
