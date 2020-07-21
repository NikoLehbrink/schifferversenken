class Gameboard(object):
  def __init__(self, board_width, board_height, battleships):
    self.board_wdith = board_width
    self.board_height = board_height
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


# Print-Funktion für das Spielbrett
def render(board_width, board_height, shots):
  field_border_top_bottom = "+" + "-" * board_width + "+"
  print(field_border_top_bottom)

# Aus Performancegründen machen wir ein Set raus
  shots_set = set(shots)

  for y in range(board_height):
    row = []
    for x in range(board_width):
      if (x,y) in shots_set:
        character = "X"
      else:
        character = " "
      row.append(character)
    print("|" + "".join(row) + "|", end=" ")
    print(row)
    # print("|" + " " * board_width + "|")

  print(field_border_top_bottom)

def render_battleships(board_width, board_height, battleships):
  field_border_top_bottom = "+" + "-" * board_width + "+"
  print(field_border_top_bottom)

  # construct empty board
  board = []
  for x in range(board_width):
    # Python spezifisches List-Comprehension, Alternative für:    
    # row = []
    # for y in range(board_height):
    #   row.append(None)
    # board.append (row)
    board.append([None for y in range(board_height)])

  # add the battleships to the board
  for b in battleships:
    for x,y in b.body:
      board[x][y] = "0"

  for y in range(board_height):
    row = []
    for x in range(board_width):
      row.append(board[x][y] or " ")
    print("|" + "".join(row) + "|")

  print(field_border_top_bottom)




if __name__=="__main__":
  battleships = [
    Battleship.build((1,2), 2, "S"),
    Battleship.build((3,4), 4, "W"),
    Battleship.build((5,7), 3, "E")
  ]

  game_board = Gameboard(10,10,battleships)
  shots = [(1,1),(0,0), (5,7)]

  for sh in shots:
    game_board.take_shot(sh)

  for sh in game_board.shots:
    print(sh.location)
    print(sh.is_hit)
    print("======")
  for b in game_board.battleships:
    print(b.body)
    print(b.hits)
    print("======")
  
  exit(0)




  print(game_board.shots)
  print(game_board.battleships)
  render_battleships(10,10, battleships)



  shots = []

  while(True):
    # ToDo: Bad user input
    inp = input("Wo willst du hinschiessen?\n")
    x_str, y_str =inp.split(",")
    x = int(x_str)
    y = int(y_str)
    shots.append((x,y))
    render(10,10, shots)