from AI.related_pkgs import *
import AI.constant as const
from AI.agent import Agent
import AI.utils as utils

Controler = Any  # AI.unit_controler.Controler

class UnitAgent(Agent):
  name: str  # the abbreviation of the unit
  id: str  # the full id in state
  weapons: Dict[str, Tuple[int, int]]  # save all weapon names with [number of ammo, cd]
  position: VectorType = None  # LLA (lon, lat, alt) position
  position_last: VectorType = np.array([-1.0,-1.0,-1.0])  # Last LLA position, used to check weather there is occean
  hp: int  # unit health
  alive: bool  # is the unit still alive
  cmd: List  # command from base_agent
  controler: Controler = None
  last_patrol_controler: Controler = None
  rotate_direction: int = 1  # 1 is the counterclockwise, -1 is the clockwise

  def __init__(self, name: str, id: str, cmd: List):
    super().__init__()
    self.name, self.id, self.cmd, self.alive = name, id, cmd, True
    self.weapons = {}
  
  def _DEBUG(self):
    position = [round(x, 6) for x in self.position]
    if self.alive:
      print("**DEBUG position**\t", self.name, self.id, position, self.weapons, self.alive, self.hp)
    else:
      print("**DEBUG position**\t", self.name, self.id, "has been destoried or boarding!")

  def deploy(self, position: VectorType):  # Won't be used in true battle.
    self.position = position
    if const.has_optional_bullet[self.name]:
      for key, val in const.weapon_unit_init[self.name].items():
        if 'PiercingShot' in key: pierce = val
        if 'ExplosiveShot' in key: explose = val
      self.cmd.append(self._ArmorCar_Deploy_Action(self.id, *position, pierce, explose))
    else:
      self.cmd.append(self._Deploy_Action(self.id, *position))
  
  @staticmethod
  def xy2xyz(xy: VectorType):
    if len(xy) == 3: return xy
    return np.array([*xy, 0])
  
  @staticmethod
  def xyz2xy(xyz: VectorType):
    if len(xyz) == 2: return xyz
    return np.array(xyz[:2])
  
  @staticmethod
  def set3zero(vector: VectorType):
    vector = np.array(vector)
    vector[2] = 0.0
    return vector
  
  def move_relative(self, direction: VectorType):
    direction = self.xy2xyz(direction)
    xyz = self.lla2xyz(self.position)
    xyz += direction
    self.move(self.xyz2lla(xyz))
  
  def get_rotation_matrix(self, mu=0, sigma=1/3, max_angle=np.pi/4):
    if np.all(self.position == self.position_last):
      self.rotate_direction *= -1.0
    angle = mu + np.clip(np.random.normal() * sigma, -1.0, 1.0) * max_angle
    angle *= self.rotate_direction
    R = np.array([
      [np.cos(angle), -np.sin(angle)],
      [np.sin(angle), np.cos(angle)],
    ])
    return R

  def move_target(self, lla: VectorType, delta_size=100, noisy=True, verbose=False):
    tmp1, tmp2 = self.set3zero(self.position), self.set3zero(lla)
    xyz, target_xyz = self.lla2xyz(tmp1), self.lla2xyz(tmp2)
    # xyz, target_xyz = self.lla2xyz(self.position), self.lla2xyz(lla)
    delta = self.xyz2xy(target_xyz) - self.xyz2xy(xyz) + np.array([1.0, 0.0])
    size = np.sqrt((delta ** 2).sum())
    # if size <= 10:  # so close, won't need move
    #   return
    delta = delta / size * delta_size
    if noisy:
      R = self.get_rotation_matrix()
      delta = (R @ delta.reshape(-1, 1)).reshape(-1)
    delta = np.array([*delta, 0])
    target_lla = self.xyz2lla(xyz + delta)
    target_lla[2] = 0
    if verbose:
      print(self.position, "to", target_lla)
    self.move(target_lla)
  
  def move_circle(
      self, center_lla: VectorType,
      radius: float,
      alpha: float = 1.0,
      
      rotate_angle: float = np.pi / 3,
      noisy: bool = True,
      verbose: bool = False,
    ):
    tmp1, tmp2 = self.set3zero(self.position), self.set3zero(center_lla)
    xyz, center_xyz = self.lla2xyz(tmp1), self.lla2xyz(tmp2)
    # xyz, center_xyz = self.lla2xyz(self.position), self.lla2xyz(center_lla)
    delta = self.xyz2xy(xyz) - self.xyz2xy(center_xyz) + np.array([1.0, 0.0])
    size = np.sqrt((delta**2).sum())
    delta = delta / size * radius * alpha
    if size <= radius:
      R = self.get_rotation_matrix(mu=rotate_angle, max_angle=np.pi / 36 if noisy else 0.0)
      delta = (R @ delta.reshape(-1, 1)).reshape(-1)
    delta = np.array([*delta, 0])
    target_lla = self.xyz2lla(center_xyz + delta)
    if not const.check_in_boundary(target_lla):
      self.rotate_direction *= -1.0
      R[0,1] *= -1.0
      R[1,0] *= -1.0
      delta = (R @ R @ delta[:2].reshape(-1, 1)).reshape(-1)
      delta = np.array([*delta, 0])
      target_lla = self.xyz2lla(center_xyz + delta)
    self.move_target(target_lla, noisy=True if size > radius else False, verbose=verbose)

  def move(self, position: VectorType):
    self.cmd.append(self._Move_Action(self.id, *position))
  
  def find_attack_weapon(self, name: str, target_position: np.ndarray):
    distance = utils.get_distance_lla(self.position, target_position)
    weapon_name, weapon_score = None, 0
    for weapon, (emmo, cd) in self.weapons.items():
      score = const.check_weapon2target(weapon, name, distance)
      if cd == 0 and emmo > 0 and score != 0:
        if score > weapon_score:
          weapon_score = score
          weapon_name = weapon
    return weapon_name

  def attack(self, position: VectorType, weapon):
    # TODO: Add attack strategy
    if weapon is None: return
    command = self._Attack_Action(self.id, *position, weapon)
    self.cmd.append(command)

  def update(self, state: dict):
    """
    Update the unit position and weapon state (Num and CD).
    """
    if self.id not in state.keys():  # GG
      self.alive = False; return
    state = state[self.id]
    self.alive = state['isActive']
    vs = state['VehicleState']
    self.position_last = self.position
    self.position = np.array((vs['lon'], vs['lat'], vs['alt']))
    self.hp = vs['hp']
    wss = state['WeaponState']
    for ws in wss:
      weapon_name = ws['WeaponType'][:-9]
      self.weapons[weapon_name] = (ws['WeaponNum'], ws['WeaponCD'])
  
  def reset(self):
    self.alive = True
    self.weapons = {}
  
  def change_state(self, new_state):  # run: 0, stop: 1, hide: 2
    command = self._Change_State(self.id, new_state)
    self.cmd.append(command)
  
  def on_board_action(self, wheel_id):
    command = self._On_Board_Action(wheel_id, self.id)
    self.cmd.append(command)
  
  def off_board_action(self, wheel_id):
    command = self._Off_Board_Action(wheel_id, self.id)
    self.cmd.append(command)
