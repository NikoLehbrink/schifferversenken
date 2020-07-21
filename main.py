  
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


if __name__=="__main__":

    shots = []

    while(True):
      # ToDo: Bad user input
      inp = input("Wo willst du hinschiessen?\n")
      x_str, y_str =inp.split(",")
      x = int(x_str)
      y = int(y_str)
      shots.append((x,y))
      render(10,10, shots)