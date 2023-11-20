from AI.related_pkgs import *
from AI.base_agent import BaseAgent
import AI.constant as const
import AI.utils as utils
from AI.unit_agent import UnitAgent
from AI.unit_controler import name2controler, PatrolControler
init_lla = const.red_initial_lla
init_controler = const.red_init_controler
aux_units = const.red_aux_unit
watch_target_ids = const.red_watch_target_ids

class RedAgent(BaseAgent):
  def __init__(self):
    super().__init__()
  
  def deploy0(self, ids):
    super().deploy(ids)
    for units in self.units.values():
      for i, unit in enumerate(units):
        if i == 0 and unit.name == 'tank':
          unit.deploy(const.target_lla)
        elif i == 1 and unit.name == 'tank':
          unit.deploy((2.60, 39.7198, 0))
        else:
          unit.deploy(init_lla[unit.id])
    return self.cmd

  def deploy1(self, ids):
    super().deploy(ids)
    for units in self.units.values():
      for i, unit in enumerate(units):
        # if unit.id == 'MainBattleTank_ZTZ100_0':
        #   unit.deploy((2.68358, 39.7006, 0))
        # else:
        unit.deploy(init_lla[unit.id])
        if unit.id in init_controler.keys():
          (controler_name, *args) = init_controler[unit.id]
          aux_unit = aux_units.get(unit.id)
          if aux_unit is not None:
            aux_unit = self.units_id[aux_unit]
          controler = name2controler[controler_name](
            unit, *args, aux_unit=aux_unit
          )
          unit.controler = controler
    return self.cmd
  
  def deploy(self, ids):  # only deploy units
    for id in ids:
      for name, aux in const.name2aux.items():
        if aux in id:
          unit = UnitAgent(name, id, self.cmd)
          unit.deploy(init_lla[id])
          break
    return self.cmd

  def step(self, state: dict):
    if self.step_num == 0:  # init controler state
      # super().deploy(list(state.keys()), init_lla, {}, aux_units)  # for test
      super().deploy(list(state.keys()), init_lla, init_controler, aux_units)
      
    self.update_state(state)
    # print("Red detection:", self.detection)

    ### Control unit by the controler ###
    for unit in self.units_flatten:
      if unit.controler is not None:
        unit.controler.step(self.detection)

    ### Watch target: we need one unit to stay in target ###
    watch_target = False
    for unit in self.units_flatten:
      if unit.controler is None or not unit.alive: continue
      if unit.controler.mode == 'patrol' and unit.controler.name == 'target':
        watch_target = True
    if not watch_target:
      for id in watch_target_ids:
        unit = self.units_id[id]
        if unit.controler is None or not unit.alive: continue
        unit.controler = PatrolControler(
          unit=unit,
          point='target',
          aux_unit=unit.controler.aux_unit,
        )
        break
    
    for unit in self.units['missile']:  # just fire!
      unit.attack(const.target_lla, 'ShortRangeMissile')
    return self.cmd
    