轨迹提取目标：
### Step1
对于所有流向，提取出从日照钢厂到其他流向的所有轨迹数据，选择较长距离流向
### Step2
查看司机数据量分布，找到历史轨迹数较多的司机
### Step3
提取出每个流向所有的停留点， 并提取出每个司机对应停留偏好序列，构成下列数据结构：
司机ID、出发时段、起终点（或者是起终点区域）、具体路径

文件展示：  
1、轨迹可视化
- vis_traj.py #绘制所有轨迹
- vis_pre_traj.py #绘制单条轨迹  

2、主要预处理文件
- remove_longdist.py #移除长距离路线
- extract_staypoint.py #提取停留点
- cluster_sp.py #对停留点进行聚类
- statics_get_poi.py #统计停留点所属的POI类别
- statics_driver_behavior.py #加上了每个轨迹点到起始点的距离
- statics_dir.py   
  - 统计每次行程中停留点个数
  - 统计司机在不同出发时段（POI类型序列的变化关系、停留时长）
- statics_tmp.py #暂时不用

3、辅助文件
- utils.py
- utils_poi.py 
- objclass.py

4、暂时不用的文件
- read_tag_file.py
