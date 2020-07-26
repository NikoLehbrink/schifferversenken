from Shot import Shot

class Gameboard(object):
  def __init__(self, width, height, battleships):
    self.width = width
    self.height = height
    self.battleships = battleships
    self.shots = []
# Todo: update battleship with any hits
# Todo: save the fact that the shot was a hit or a miss
  def take_shot(self, shot_location):
    hit_battleship = None
    is_hit = False
    for b in self.battleships:
        index = b.body_index(shot_location)
        if index is not None:
          is_hit = True
          b.hits[index] = True
          hit_battleship = b
          # Breakt raus, weil wir wissen welches Schiff getroffen wurde
          break
    
    self.shots.append(Shot(shot_location, is_hit))
    return hit_battleship

  def is_game_over(self):
    for b in self.battleships:
      if not b.is_destroyed():
        return False
    return True
