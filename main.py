import copy
import random

class Gameboard(object):
  def __init__(self, width, height, battleships):
    self.width = width
    self.height = height
    self.battleships = battleships
    self.shots = []
# Todo: update battleship with any hits
# Todo: save the fact that the shot was a hit or a miss
  def take_shot(self, shot_location):
    is_hit = False
    for b in self.battleships:
        index = b.body_index(shot_location)
        if index is not None:
          is_hit = True
          b.hits[index] = True
          # Breakt raus, weil wir wissne welches Schiff getroffen wurde
          break
    
    self.shots.append(Shot(shot_location, is_hit))
    return is_hit

  def is_game_over(self):
    for b in self.battleships:
      if not b.is_destroyed():
        return False
    return True


class Shot(object):
  def __init__(self, location, is_hit):
    self.location = location
    self.is_hit = is_hit

class Battleship(object):

  @staticmethod
  def build(head, length, direction):
    body = []
    for i in range(length):
      # Wenn direction Nord ist, bleib die x-Koordinate gleich, aber die y-Koordinate ändert sich um die Anzahl der Länge
      if direction == "N":
        # head[0] ist x-Koordinate des Schiffbeginns, welcher der User festlegt, head[1] ist die y-koordinate
        element = (head[0], head[1] - i)
      elif direction == "S":
        element = (head[0], head[1] + i)
      elif direction == "W":
        element = (head[0] - i, head[1])
      elif direction == "E":
        element = (head[0] + i, head[1])

      body.append(element)
    return Battleship(body, head, length, direction)


# Todo: which of this params do we actually need?
  def __init__(self, body, head, length, direction):
    self.body = body
    self.head = head
    self.length = length
    self.direction = direction
    self.hits = [False] * len(body)

  def body_index(self, location):
    try:
      return self.body.index(location)
    except ValueError:
      return None
  
  def is_destroyed(self):
    for ht in self.hits:
      if(ht == False):
        return False
    return True

class Player(object):

  def __init__(self, name, shot_function):
    self.name = name
    self.shot_function = shot_function

def render(game_board, show_battleships=False):
  field_border_top_bottom = "+" + "-" * game_board.width + "+"
  print(field_border_top_bottom)

  board = []
  for x in range(game_board.width):
    board.append([None for y in range(game_board.height)])

  if(show_battleships):
    # add the battleships to the board
    for b in game_board.battleships:
      # Durch enmuerate macht man counter variable und wenn anfang oder ende des schiffes → mach andere zeichen
      for i,(x,y) in enumerate(b.body):
        if b.direction == "N":
          characters = ("v", "|", "^")
        if b.direction == "S":
          characters = ("^", "|", "v")
        if b.direction == "E":
          characters = ("<", "-", ">")
        if b.direction == "W":
          characters = (">", "-", "<")

        if i == 0:
          character= characters[0]
        elif i == len(b.body) - 1:
          character = characters[2]
        else:
          character = characters[1]
        board[x][y] = character

  # Add shots to the board
  for sh in game_board.shots:
    x, y = sh.location
    if sh.is_hit:
      character = "X"
    else:
      character = "."
    board[x][y] = character

  for y in range(game_board.height):
    row = []
    for x in range(game_board.width):
      row.append(board[x][y] or " ")
    print("|" + "".join(row) + "|")

  print(field_border_top_bottom)


def get_random_ai_shot(game_board):
  x = random.randint(0, game_board.width - 1 )
  y = random.randint(0, game_board.height - 1)
  return (x,y)

def get_human_shot(game_board):
  inp = input("Wo willst du hinschiessen?\n")
  x_str, y_str = inp.split(",")
  x = int(x_str)
  y = int(y_str)
  return (x,y)

if __name__=="__main__":

  battleships = [
    Battleship.build((1,0), 3, "S"),
    Battleship.build((3,4), 4, "N"),
    Battleship.build((5,7), 3, "E")
  ]

  game_boards = [
    Gameboard(10,10,battleships),  
    Gameboard( 10,10,copy.deepcopy(battleships))  
  ]

  players = [
    Player("Rob", get_human_shot),
    Player("Niko", get_random_ai_shot)
  ]
  offensive_index = 0

  while(True):
    # Immer die Zahl, die der Gegenpart nicht ist
    defensive_index = (offensive_index + 1) % 2

    defensive_board = game_boards[defensive_index]
    offensive_player = players[offensive_index]

    print("%s Yoour Turn!" % offensive_player.name)

    shot_location = offensive_player.shot_function(defensive_board)
    # ToDo: Bad user input

    x = defensive_board.take_shot(shot_location)
    render(defensive_board, True)

    if defensive_board.is_game_over():
      print("%s You Win" % offensive_player.name)
      break
    if x == False:
      offensive_index = defensive_index