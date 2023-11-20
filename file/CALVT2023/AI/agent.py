import math
import numpy as np
import AI.constant as const

class Agent(object):
  def __init__(self):
    self.infantry_tank_map = {}
    self.groupmap = {}
    self.time_ = 0
    
  @staticmethod
  def LLA2XYZ(lon, lat, alt):
    Earthe = 0.0818191908426
    Radius_Earth = 6378140.0
    PI = 3.14159265358979
    deg2rad = PI / 180.0
    lat = lat * deg2rad
    lon = lon * deg2rad
    omge = 0.99330562000987
    d = Earthe * math.sin(lat)
    n = Radius_Earth / math.sqrt(1 - math.pow(d, 2))
    nph = n + alt
    x = nph * math.cos(lat) * math.cos(lon)
    y = nph * math.cos(lat) * math.sin(lon)
    z = (omge * n + alt) * math.sin(lat)
    return x, y, z
  
  @staticmethod
  def XYZ2LLA(x, y, z):
    Radius_Earth = 6378140
    Oblate_Earth = 1.0 / 298.257
    a = Radius_Earth
    b = a * (1 - Oblate_Earth)
    e = math.sqrt(1 - math.pow(b / a, 2))
    x2 = x * x
    y2 = y * y
    root = math.sqrt(x2 + y2)
    e2 = e * e
    error = 1.0
    d = 0.0
    B = 0.0
    H = 0.0
    eps = 1e-10
    PI = 3.14159265358979
    deg2rad = PI / 180.0
    rad2deg = 180.0 / PI

    while error >= eps:
      temp = d
      B = math.atan(z / root / (1 - d))
      sin2B = math.sin(B) * math.sin(B)
      N = a / math.sqrt(1 - e2 * sin2B)
      H = root / math.cos(B) - N
      d = N * e2 / (N + H)
      error = abs(d - temp)
    lat = B
    alt = H
    temp = math.atan(y / x)
    if x >= 0:
      lon = temp
    elif ((x < 0) and (y >= 0)):
      lon = PI + temp
    else:
      lon = temp - PI
    lat = lat * rad2deg
    lon = lon * rad2deg
    alt = alt
    return lon, lat, alt

  @staticmethod
  def lla2xyz(position: np.ndarray):
    return np.array(Agent.LLA2XYZ(*position))

  @staticmethod
  def xyz2lla(position: np.ndarray):
    return np.array(Agent.XYZ2LLA(*position))

  def distance(self, lon1, lat1, alt1, lon2, lat2, alt2):
    x1, y1, z1 = self.LLA2XYZ(lon1, lat1, alt1)
    x2, y2, z2 = self.LLA2XYZ(lon2, lat2, alt2)
    x2tox1 = x2 - x1
    y2toy1 = y2 - y1
    z2toz1 = z2 - z1
    distance = math.sqrt(x2tox1 * x2tox1 + y2toy1 * y2toy1 + z2toz1 * z2toz1)
    return distance

  # 装甲车部署指令函数
  # TODO: 高度、地理信息；改接口
  def _ArmorCar_Deploy_Action(self, id, lon, lat, alt, PierceShotNum, ExplosiveShotNum):
    ArmorCarDeployAction = {"Type": "ArmorCar_Deploy", "Id": id, "Lon": lon, "Lat": lat, "Alt": alt,
              "PierceShotNum": PierceShotNum, "ExplosiveShotNum": ExplosiveShotNum}
    return ArmorCarDeployAction

  # 非装甲单位部署指令
  def _Deploy_Action(self, id, lon, lat, alt):
    DeployAction = {"Type": "Deploy", "Id": id, "Lon": lon, "Lat": lat, "Alt": alt}
    return DeployAction

  # 移动指令函数
  def _Move_Action(self, Id, lon, lat, alt):
    MoveAction = {"Type": "Move", "Id": Id, "Lon": lon, "Lat": lat, "Alt": alt}
    return MoveAction

  def _Change_State(self,Id,vehicleMoveState ):
    ChangeState = {"Type": "Change", "Id":  Id,"VehicleMoveState":vehicleMoveState}
    return ChangeState

  # 释放飞机指令函数
  def _Plane_Launch_Action(self, Id, Plane_Type, lon, lat, alt):
    planeLaunchAction = {"Type": "Launch_plane", "Id": Id, "Plane_Type": Plane_Type, "Lon": lon, "Lat": lat, "Alt": alt}
    return planeLaunchAction

  # 火力分配指令函数
  def _Attack_Action(self, Id, lon, lat, alt,Unit_Type):
    AttackAction = {"Type": "Attack", "Id": Id, "Unit_Type": Unit_Type, "Lon": lon, "Lat": lat, "Alt": alt}
    return AttackAction

  # 编队指令
  def _Combine_Action(self, Id, groupId):
    CombineAction = {"Type": "Combine_", "Id": Id, "groupId": groupId}
    # print("command combine")
    self._insert_to_groupmap(Id, groupId)  # groupid 合法性由qt 判断
    # print("current group ",self.groupmap)
    return CombineAction

  def _Del_Combine_Action(self, groupId):
    DelCombineAction = {"Type": "DelCombine", "groupId": groupId}
    # print("command delcombine")
    self._remove_from_groupmap(groupId)
    # print("current group ",self.groupmap)
    return DelCombineAction
  # 上下车指令
  def _On_Board_Action(self, tankid, infantryid):
    onBoardAction = {"Type": "On_Board", "tankid": tankid, "infantryid": infantryid}
    self._insert_to_infantankmap(tankid, infantryid)
    return onBoardAction

  def _Off_Board_Action(self, tankid, infantryid = -1):
    offBoardAction = {"Type": "Off_Board", "tankid": tankid, "infantryid": infantryid}
    self._remove_from_infantrytankmap(tankid, infantryid)
    return offBoardAction


  # szh
  def _insert_to_groupmap(self, unitid, groupid):
    if groupid not in self.groupmap.keys():
      self.groupmap[groupid] = []
    self.groupmap[groupid].append(unitid)
    return

  def _remove_from_groupmap(self, groupid):
    # print("in remove from group ", groupid)
    if groupid not in self.groupmap.keys():
      return
    self.groupmap.pop(groupid)
    return

  def _insert_to_infantankmap(self, tankid, infantryid):
    if tankid not in self.infantry_tank_map.keys():
      self.infantry_tank_map[tankid] = []   ##  目前限制步战车上步兵班数量为1
    if tankid in self.infantry_tank_map.keys() and len(self.infantry_tank_map[tankid]) > 0:
      return
    self.infantry_tank_map[tankid].append(infantryid)
    return

  def _remove_from_infantrytankmap(self, tankid, infantryid = -1):
    if tankid not in self.infantry_tank_map.keys():
      return
    else:
      self.infantry_tank_map.pop(tankid)
    return

  # 获取舰船探测信息函数 status红蓝方态势信息
  def get_detect_info(self, status):
    # LJD不会探测
    WheeledCombatTruckID = [id for id in status if "WheeledCombatTruck" in id]
    ArmoredTruckID = [id for id in status if "ArmoredTruck" in id]
    MissleTruckID = [id for id in status if "missile_truck" in id]
    InfantryID = [id for id in status if "Infantry" in id and "Bullet_Infantry" not in id]
    MainBattleTankID = [id for id in status if "MainBattleTank" in id]
    HowitzerID = [id for id in status if "Howitzer" in id]
    ShipboardCombatPlaneID = [id for id in status if "ShipboardCmobat_plane" in id]
    HeavyDestroyerID = [id for id in status if "HeavyDestroyer" in id]
    unit_id_list = WheeledCombatTruckID + ArmoredTruckID + MissleTruckID + InfantryID + MainBattleTankID + \
           ShipboardCombatPlaneID + HeavyDestroyerID + HowitzerID

    # UPDATE: Build up detectinfo clearly.
    detectinfo = {name: {} for name in const.aux2name.keys()}
    for unit in unit_id_list:
      for detector in status[unit]['DetectorState']:
        for target in detector['DetectedState']:
          target_id = target['targetID']
          # print("**DEBUG detection**\t", unit, "detect:", target_id)
          lla = np.array([target['targetLon'], target['targetLat'], target['targetAlt']])
          # lla_last = np.array([target['targetLastLon'], target['targetLastLat'], target['targetLastAlt']])
          # lla_pred = lla if lla_last[0] == -1 else 2 * lla - lla_last
          pos = np.array(lla)
          # pos = np.stack([lla, lla_last, lla_pred], axis=0)
          for name in detectinfo.keys():
            if const.name2aux[name] in target_id:
              detectinfo[name][target_id] = pos
              break
          # detectinfo[target_id] = target
    for key in list(detectinfo.keys()):
      if len(detectinfo[key]) == 0:
        detectinfo.pop(key)
    return detectinfo

if __name__ == '__main__':
  a = Agent()