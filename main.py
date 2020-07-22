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
    return Battleship(body)

  def __init__(self, body):
    self.body = body
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




def render(game_board, show_battleships=False):
  field_border_top_bottom = "+" + "-" * game_board.width + "+"
  print(field_border_top_bottom)

  board = []
  for x in range(game_board.width):
    board.append([None for y in range(game_board.height)])

  if(show_battleships):
    # add the battleships to the board
    for b in game_board.battleships:
      for x,y in b.body:
        board[x][y] = "0"

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

def render_battleships(width, height, battleships):
  field_border_top_bottom = "+" + "-" * width + "+"
  print(field_border_top_bottom)

  # construct empty board
  board = []
  for x in range(width):
    board.append([None for y in range(height)])

  # add the battleships to the board
  for b in battleships:
    for x,y in b.body:
      board[x][y] = "0"

  for y in range(height):
    row = []
    for x in range(width):
      row.append(board[x][y] or " ")
    print("|" + "".join(row) + "|")

  print(field_border_top_bottom)

if __name__=="__main__":
  battleships = [
    Battleship.build((1,2), 2, "S"),
    # Battleship.build((3,4), 4, "W"),
    # Battleship.build((5,7), 3, "E")
  ]

  game_board = Gameboard(10,10,battleships)

  while(True):
    # ToDo: Bad user input
    inp = input("Wo willst du hinschiessen?\n")
    x_str, y_str = inp.split(",")
    x = int(x_str)
    y = int(y_str)
    game_board.take_shot((x,y))
    render(game_board)

    if game_board.is_game_over():
      print("You Win")
      break