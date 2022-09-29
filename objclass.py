class TrajPoint:
    def __init__(self, plan_no, waybill_no, longitude, latitude, time):
        self.plan_no = plan_no
        self.waybill_no = waybill_no
        self.longitude = longitude
        self.latitude = latitude
        self.time = time

class Traj:
    def __init__(self, plan_no, waybill_no, dri_id):
        self.plan_no = plan_no
        self.waybill_no = waybill_no
        self.dri_id = dri_id
        self.traj_point_list = []

# 存放所有轨迹
class TrajAll:
    def __init__(self):
        self.traj_dict = {}

# 停留点类
class StayPoint:
    def __init__(self, cen_lng, cen_lat, start_staytime, duration, waybill_no, plan_no, dri_id,
                 staypoilist=None, cluster_id=None,
                 matched_road_id=None):
        self.cen_lng = cen_lng  # 中心点经度 float
        self.cen_lat = cen_lat  # 中心点纬度 float
        self.start_staytime = start_staytime  # 停留发生时间 datetime
        self.duration = duration  # 停留时间 float
        self.waybill_no = waybill_no  # 运单号
        self.plan_no = plan_no  # 调度单号
        self.dri_id = dri_id  # 司机ID
        self.staypoilist = staypoilist  # 低速轨迹点列表 list
        self.cluster_id = cluster_id  # 聚类编号
        self.matched_road_id = matched_road_id

# 停留区域
class StayRegion:
    def __init__(self, sr_id, cen_lng=None, cen_lat=None):
        self.sr_id = sr_id  # 地点ID
        self.cen_lng = cen_lng  # 区域的中心点经度
        self.cen_lat = cen_lat  # 区域的中心点纬度
        self.staypoiobj_list = []  # 该区域中停留点实体(staypoi类的实体)的列表
        self.vertex_list = []  # 多边形顶点的列表 存放Point
        self.type = None  # 停留区域类型
        self.convex_hull = None  # convex_hull
        self.polygon = None
        self.feature = []  # 特征向量
        self.num_staypoint = 0  # 停留点个数
        self.nearRoad_type = None  # string
        self.nearPoiType_distribute = None  # list
        self.area = None  # 区域面积 float
        self.turn_position = None  # 转向位置
        self.pid = {}  # 统计pid出现过的次数
        self.planno_set = set()  # 存放调度单的集合，防止被重复传入
        self.score = 0  # 计算候选位置得分
