from AI.related_pkgs import *

name2aux = {
  'tank': 'MainBattleTank',
  'howitzer': 'Howitzer',
  'infantry': 'Infantry',
  'armor': 'ArmoredTruck',
  'wheel': 'WheeledCmobatTruck',
  'missile': 'missile_truck',
  'plane': 'ShipboardCombat_plane',
}
aux2name = {aux: name for aux, name in name2aux.items()}
has_optional_bullet = {
  'tank': True, 'howitzer': True,
  'infantry': False, 'armor': False, 'wheel': False,
  'missile': False, 'plane': False,
}

weapon_unit_init = {
  'tank': {
    'Bullet_ZT': 2500,
    'ArmorPiercingShot_ZT': 30,  # sum up: 60
    'HighExplosiveShot_ZT': 30,
  },
  'howitzer': {
    'Bullet_ZT': 2500,
    'ArmorPiercingShot': 40,  # sum up: 80
    'HighExplosiveShot': 40,
  },
  'infantry': {
    'bullet': 1500,
    'RPG': 4,
  },
  'armor': {
    'Bullet_ZT': 2500,
    'RPG': 2,
  },
  'wheel': {
    'Bullet_ZT': 2500,
  },
  'missile_red': {
    'ShortRangeMissile': 16,
  },
  'missile_blue': {
    'LDJS_sm6': 16,
  },
  'plane': {
    'AGM': 4,
  }
}

# (min_range, max_range)
# `min_range` < `target_distance` <= `max_range`
bullet_range = {
  'bullet': (0, 400),
  'Bullet_ZT': (0, 700),
  'ShortRangeMissile': (0, 600000),
  'AGM': (0, 15000),
  'RPG': (0, 400),
  'ArmorPiercingShot': (0, 2800),
  'ArmorPiercingShot_ZT': (0, 2800),
  'HighExplosiveShot': (0, 2800),
  'HighExplosiveShot_ZT': (0, 2800),
}

map_corner = np.array([
  [(2.6, 39.85, 0.0), (2.8, 39.85, 0.0)],
  [(2.6, 39.65, 0.0), (2.8, 39.65, 0.0)]
])

target_lla = [2.71, 39.76, 100]  # [2.71, 39.76, 100]

red_initial_lla = {  # 15 units
  'missile_truck0': [2.6228, 41.6363, 0],  # This three missile can't move!
  'missile_truck1': [2.6238, 41.6373, 0],  # They are safe, nobody can attack them.
  'missile_truck2': [2.6238, 41.6373, 0],
  'WheeledCmobatTruck_ZB100_0': [2.59, 39.72, 0],
  'WheeledCmobatTruck_ZB100_1': [2.59, 39.72, 0],
  'Infantry0': [2.59, 39.72, 0],
  'Infantry1': [2.59, 39.72, 0],
  'MainBattleTank_ZTZ100_0': [2.59, 39.72, 0],
  'MainBattleTank_ZTZ100_1': [2.59, 39.72, 0],
  'MainBattleTank_ZTZ100_2': [2.59, 39.72, 0],
  'MainBattleTank_ZTZ100_3': [2.59, 39.72, 0],
  'ArmoredTruck_ZTL100_0': [2.59, 39.72, 0],
  'ArmoredTruck_ZTL100_1': [2.59, 39.72, 0],
  'ShipboardCombat_plane0': [2.59, 39.72, 3000],
  'Howitzer_C100_0': [2.59, 39.72, 0],
}

blue_initial_lla = {  # 18 units
  'WheeledCmobatTruck_ZB200_0': [2.68818, 39.7026, 0],
  'WheeledCmobatTruck_ZB200_1': [2.68818, 39.7026, 0],
  'WheeledCmobatTruck_ZB200_2': [2.68818, 39.7026, 0],
  'WheeledCmobatTruck_ZB200_3': [2.68818, 39.7026, 0],
  'Infantry2': [2.68618, 39.7006, 0],
  'Infantry3': [2.68618, 39.7006, 0],
  'Infantry4': [2.68618, 39.7006, 0],
  'Infantry5': [2.68618, 39.7006, 0],
  'MainBattleTank_ZTZ200_0': [2.68984, 39.70, 0],
  'MainBattleTank_ZTZ200_1': [2.68984, 39.70, 0],
  'MainBattleTank_ZTZ200_2': [2.68984, 39.70, 0],
  'MainBattleTank_ZTZ200_3': [2.68984, 39.70, 0],
  'ShipboardCombat_plane1': [2.68995, 39.7, 3000],
  'missile_truck3': [2.68995, 39.7, 0],
  'missile_truck4': [2.68995, 39.7, 0],
  'missile_truck5': [2.68995, 39.7, 0],
  'missile_truck6': [2.68995, 39.7, 0],
  'missile_truck7': [2.68995, 39.7, 0],
}

detection_range = {
  'tank': 2500,
  'howitzer': 400,
  'infantry': 400,
  'armor': 400,
  'wheel': 400,
  'missile': 400,
  'plane': 3000,
}

search_path = {
  'path0': [(2.7094, 39.7595), (2.7094, 39.7603), (2.7105, 39.7603), (2.7105, 39.7595)],
  'path1': [(2.7085, 39.7587), (2.7085, 39.7613), (2.7113, 39.7613), (2.7113, 39.7587)],
}
patrol_point = {
  'target': (target_lla, 80.0),
  'target_400': (target_lla, 400.0),
  'target_800': (target_lla, 800.0),
  'point0': ((2.7119, 39.7618), 1000.0),
  'point1': ((2.7067, 39.7566), 1000.0),
  'point2': ((2.7127, 39.7553), 1000.0),
  'save_point': ((2.7273, 39.7395), 1000.0),
  'red_init_400': ((2.59, 39.72), 400.0),
  'red_init_2000': ((2.59, 39.72), 2000.0),
  'blue_init_400': ((2.68658, 39.7006), 400.0),
  'blue_init_2000': ((2.68658, 39.7006), 2000.0),
}
blue_aux_unit = {
  'WheeledCmobatTruck_ZB200_0': 'Infantry2',
  'WheeledCmobatTruck_ZB200_1': 'Infantry3',
  'WheeledCmobatTruck_ZB200_2': 'Infantry4',
  'WheeledCmobatTruck_ZB200_3': 'Infantry5',
}
blue_init_controler = {
  'WheeledCmobatTruck_ZB200_0': # ('search', 'path0'),
    ('patrol', 'point0'),
  'WheeledCmobatTruck_ZB200_1': # ('search', 'path0'),
    ('patrol', 'point0'),
  'WheeledCmobatTruck_ZB200_2': # ('search', 'path1'),
    ('patrol', 'point1'),
  'WheeledCmobatTruck_ZB200_3': # ('search', 'path1'),
    ('patrol', 'point1'),
  'MainBattleTank_ZTZ200_0':
    ('patrol', 'red_init_400'),
  'MainBattleTank_ZTZ200_1':
    ('search', [(2.6711, 39.7464), (2.6258, 39.7317)]),
  'MainBattleTank_ZTZ200_2':
    ('patrol', 'red_init_400'),
  'MainBattleTank_ZTZ200_3':
    ('patrol', 'red_init_400'),
  'ShipboardCombat_plane1': 
    ('patrol', 'red_init_2000'),
  'missile_truck3': 
    ('patrol', 'point0'),
  'missile_truck4': 
    ('patrol', 'point0'),
  'missile_truck5':
    ('patrol', 'point1'),
  'missile_truck6':
    ('patrol', 'point2'),
  'missile_truck7':
    ('patrol', 'point2'),
}
blue_watch_target_ids = [
  'missile_truck3',
  'missile_truck4',
  'missile_truck5',
  'missile_truck6',
  'missile_truck7',
  'WheeledCmobatTruck_ZB200_0',
  'WheeledCmobatTruck_ZB200_1',
  'WheeledCmobatTruck_ZB200_2',
  'WheeledCmobatTruck_ZB200_3',
  'MainBattleTank_ZTZ200_0',
  'MainBattleTank_ZTZ200_1',
  'MainBattleTank_ZTZ200_2',
  'MainBattleTank_ZTZ200_3',
]

red_aux_unit = {
  'WheeledCmobatTruck_ZB100_0': 'Infantry0',
  'WheeledCmobatTruck_ZB100_1': 'Infantry1',
}
red_init_controler = {
  'ArmoredTruck_ZTL100_0': # ('search', 'path0'),
    ('patrol', 'point0'),
  'ArmoredTruck_ZTL100_1': # ('search', 'path1'),
    ('patrol', 'point1'),
  'MainBattleTank_ZTZ100_0':
    ('patrol', 'blue_init_400'),
  'MainBattleTank_ZTZ100_1':
    ('patrol', 'blue_init_400'),
  'MainBattleTank_ZTZ100_2':
    ('patrol', 'blue_init_400'),
  'MainBattleTank_ZTZ100_3':
    ('patrol', 'blue_init_400'),
  'ShipboardCombat_plane0': 
    ('patrol', 'blue_init_2000'),
  'Howitzer_C100_0': 
    ('patrol', 'point0'),
  'WheeledCmobatTruck_ZB100_0':
    ('patrol', 'point0'),
  'WheeledCmobatTruck_ZB100_1':
    ('patrol', 'point1'),
}
red_watch_target_ids = [
  'Howitzer_C100_0',
  'WheeledCmobatTruck_ZB100_0',
  'WheeledCmobatTruck_ZB100_1',
  'ArmoredTruck_ZTL100_0',
  'ArmoredTruck_ZTL100_1',
  'MainBattleTank_ZTZ100_0',
  'MainBattleTank_ZTZ100_1',
  'MainBattleTank_ZTZ100_2',
  'MainBattleTank_ZTZ100_3',
]

boundary = [  # left, right, down, up
  2.59, 2.8, 39.65, 39.85
]

def check_in_boundary(lla):
  return boundary[0] <= lla[0] <= boundary[1] and boundary[2] <= lla[1] <= boundary[3]

def check_weapon2target(weapon, name, distance):
  """
  Return 0 means can't attact, [1,2,3] is the score for the weapon to attack the enermy.
  Use higher score to choose correct weapon, if there are multi weapons.
  """
  if weapon in [
    'ArmorPiercingShot_ZT', 'HighExplosiveShot_ZT',
    'ArmorPiercingShot', 'HighExplosiveShot',
    'AGM'
  ]:
    if distance > 15000: return False
    if distance > 2800 and weapon != 'AGM': return False
    if name in ['tank', 'howitzer', 'armor', 'wheel', 'missile']:
      if 'Piercing' in weapon:  # using piercing emmo to attack cars is better
        return 2
      return 1
    if name == 'infantry':  # using explosive emmo to attack infantry is better
      if 'Explosive' in weapon:
        return 2
      return 1
  if weapon in [
    'Bullet_ZT', 'bullet'
  ]:
    if distance > 700: return 0
    if distance > 400 and weapon == 'bullet': return 0
    if name in ['infantry']:
      return 3
  if weapon in [  # attack every thing
    'ShortRangeMissile', 'RPG'
  ]:
    if distance > 600000: return 0
    if distance > 1000 and weapon == 'RPG': return 0
    if weapon == 'RPG' and name == 'plane': return 0
    return 1
  return 0

if __name__ == '__main__':
  print(map_corner[0,0])