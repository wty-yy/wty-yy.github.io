from AI.unit_agent import UnitAgent
from AI.related_pkgs import *
import AI.constant as const
import AI.utils as utils

class Controler():
  unit: UnitAgent
  aux_unit: UnitAgent  # infantry, if first unit is wheel
  mode: str  # search, patrol, follow
  boarding: bool  # if aux unit is infantry

  def __init__(self, unit, aux_unit=None):
    self.unit, self.aux_unit = unit, aux_unit
    self.update_boarding_state()
  
  def step(self, detection):
    pass

  def update_boarding_state(self):
    self.boarding = True
    if self.aux_unit is not None:
      if self.aux_unit.alive:
        self.boarding = False

  def board(self):
    self.update_boarding_state()
    if self.boarding: return
    distance = utils.get_distance_lla(self.unit.position, self.aux_unit.position)
    if distance < 200:
      self.unit.change_state(1)
      self.aux_unit.on_board_action(self.unit.id)
    else:
      self.unit.move_target(self.aux_unit.position)

class SearchControler(Controler):
  path: Sequence[VectorType]
  name: str  # path0, path1, custom
  idx: int = 0
  radius: float = 200.0

  def __init__(self, unit, path, radius = 100.0, aux_unit = None):
    self.mode = 'search'
    super().__init__(unit, aux_unit)
    self.path, self.radius = path, radius
    if type(self.path) == str:
      self.name = self.path
      self.path = const.search_path[self.name]
    else:
      self.name = 'custom'
    self.idx = 0
    for i in range(len(self.path)):
      if len(self.path[i]) == 2:
        self.path[i] = np.array([*self.path[i], 0])
  
  def step(self, detection):
    if not self.boarding:
      self.board(); return
    target_lla = self.path[self.idx]
    distance = utils.get_distance_lla(self.unit.position, target_lla)
    if distance <= self.radius:
      self.idx = (self.idx + 1) % len(self.path)
      target_lla = self.path[self.idx]
    # print(self.unit.id, distance, self.unit.position, target_lla)
    self.unit.move_target(target_lla)

class PatrolControler(Controler):
  point: VectorType
  name: str  # target, point0, point1, point2, custom
  radius: float = 100.0

  def __init__(self, unit, point, radius=100.0, aux_unit = None):
    self.mode = 'patrol'
    super().__init__(unit, aux_unit)
    self.point, self.radius = point, radius
    if type(self.point) == str:
      self.name = self.point
      self.point, self.radius = const.patrol_point[self.name]
    else:
      self.name = 'custom'
    if len(self.point) == 2:
      self.point = np.array([*self.point, 0])
  
  def step(self, detection):
    if not self.boarding:
      self.board(); return
    self.unit.move_circle(self.point, self.radius)

class FollowControler(Controler):
  target_name: str
  target_id: str
  last_position: VectorType
  attack_delta: int = 5.0
  name: str = None

  def __init__(self, unit, target_name, target_id, last_position, aux_unit=None):
    self.mode = 'follow'
    self.target_name, self.target_id, self.last_position = (
      target_name, target_id, last_position
    )
    self.attack_time = 0
    super().__init__(unit, aux_unit)
  
  def step(self, detection):
    if not self.boarding:
      self.board(); return
    now_position = None
    if self.target_name in detection.keys():
      units = detection[self.target_name]
      if self.target_id in units.keys():
        now_position = units[self.target_id]
    if now_position is not None:
      if utils.get_distance_lla(now_position, self.last_position) <= self.attack_delta:
        # predict_position = 2 * now_position - self.last_position
        predict_position = now_position
        weapon = self.unit.find_attack_weapon(self.target_name, predict_position)
        if weapon is not None:
          self.unit.attack(predict_position, weapon)
      self.last_position = now_position
    self.unit.move_circle(self.last_position, const.detection_range[self.unit.name])


name2controler = {
  'search': SearchControler,
  'patrol': PatrolControler,
  'follow': FollowControler,
}