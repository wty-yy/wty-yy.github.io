from AI.related_pkgs import *
from AI.agent import Agent
from AI.unit_agent import UnitAgent
from AI.unit_controler import PatrolControler, FollowControler, name2controler
import AI.constant as const
import AI.utils as utils

class BaseAgent(Agent):
  """
  self.units = {  # classify by the unit name
    'tank': [unit_agent1, unit_agent2, ...],
    'infanty': [unit_agent3, unit_agent4, ...],
    ...
  }
  self.units_flatten = [unit_agent1, unit_agent2, unit_agent3, ...]
  """
  units: Dict[str, List[UnitAgent]]
  units_flatten: List[UnitAgent]  # flatten all the units to list
  units_id: Dict[str, UnitAgent]
  cmd: List[Command]  # the command list
  step_num: int  # total number of steps
  state: dict  # update state at each step
  detection: Dict[str, Dict[str, np.ndarray]]  # detect after update state
  detection_history: Dict[str, Dict[str, Any]]  # memory the last detection position for each id
  # {'EnermyID': {'pos': VectorType, 'name': str, 'time': int, 'follow': OurID}, ...}
  detection_forget_time: int = 40  # the maximum time to forget the last detection position

  def __init__(self):
    super().__init__()
    self.cmd = []
    np.random.seed(42)
  
  def reset(self):
    self.step_num = 0
    self.units = {}
    self.units_flatten = []
    self.units_id = {}
    self.detection_history = {}
  
  def deploy(self, ids, init_lla, init_controler, aux_units):
    self.cmd.clear()
    for name in const.name2aux.keys():
      self.units[name] = [
        UnitAgent(name, id, self.cmd) for id in ids if const.name2aux[name] in id
      ]
      self.units_flatten += self.units[name]
      for unit in self.units[name]:
        self.units_id[unit.id] = unit

        # init controler state
        unit.position = init_lla[unit.id]
        if unit.id in init_controler.keys():
          (controler_name, *args) = init_controler[unit.id]
          aux_unit = aux_units.get(unit.id)
          if aux_unit is not None:
            aux_unit = self.units_id[aux_unit]
          controler = name2controler[controler_name](
            unit, *args, aux_unit=aux_unit
          )
          unit.controler = controler
  
  def update_state(self, state):
    self.cmd.clear()
    self.state = state
    for unit in self.units_flatten:
      unit.update(state)
    self.step_num += 1
    self.detection = self.get_detect_info(state)

    ### Manage detection history ###
    for unit_name, units in self.detection.items():
      for id, pos in units.items():
        if id in self.detection_history.keys():
          self.detection_history[id]['pos'] = pos
        else:
          self.detection_history[id] = {
            'pos': pos,
            'name': unit_name,
            'time': self.step_num,
            'follow': None,
          }

    forget_ids = []
    for id, info in self.detection_history.items():
      if self.step_num - info['time'] > self.detection_forget_time:
        forget_ids.append(id)

    for id in forget_ids:
      info = self.detection_history.pop(id)
      unit = info['follow']
      if unit is not None:
        # if unit.last_patrol_controler is not None:
        #   unit.controler = unit.last_patrol_controler
        # if self.step_num > 1500:
        unit.controler = PatrolControler(unit, 'save_point')
    
    for id, info in self.detection_history.items():
      if info['follow'] is None:
        follow_unit, min_distance = None, 1e9
        for unit in self.units_flatten:
          if unit.controler is None or unit.name == 'infantry':  # infantry use wheel instead
            continue
          if (
            unit.alive and
            unit.controler.mode in ['search', 'patrol'] and
            not (unit.controler.mode == 'patrol' and unit.controler.name == 'target')
          ):
            weapon = unit.find_attack_weapon(info['name'], unit.position)
            if weapon is None: continue
            distance = utils.get_distance_lla(unit.position, info['pos'])
            if distance < min_distance:
              min_distance = distance
              follow_unit = unit

        if follow_unit is not None:
          info['follow'] = follow_unit
          if follow_unit.controler.mode == 'patrol':
            follow_unit.last_patrol_controler = follow_unit.controler  # save last patrol controler
          follow_unit.controler = FollowControler(
            unit=follow_unit,
            target_name=info['name'],
            target_id=id,
            last_position=info['pos'],
            aux_unit=follow_unit.controler.aux_unit
          )
          # print(follow_unit.id, "follow", id)
