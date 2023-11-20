from AI.related_pkgs import *
from AI.agent import Agent

def get_distance_lla(lla1: VectorType, lla2: VectorType) -> float:
  lla1, lla2 = np.array(lla1), np.array(lla2)
  if lla1[2] == 0: lla1[2] = lla2[2]
  if lla2[2] == 0: lla2[2] = lla1[2]
  xyz1, xyz2 = Agent.lla2xyz(lla1), Agent.lla2xyz(lla2)
  return np.sqrt(((xyz1 - xyz2) ** 2).sum())

if __name__ == '__main__':
  lla1 = (2.68618, 39.7006, 0)
  lla2 = (2.68818, 39.7026, 0)
  print(get_distance_lla(lla1, lla2))
