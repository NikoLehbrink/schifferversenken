class Battleship(object):

  @staticmethod
  def build(head, length, direction):
    body= []
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

  render_battleships(10,10, battleships)

  shots = []

"""   while(True):
    # ToDo: Bad user input
    inp = input("Wo willst du hinschiessen?\n")
    x_str, y_str =inp.split(",")
    x = int(x_str)
    y = int(y_str)
    shots.append((x,y))
    render(10,10, shots) """