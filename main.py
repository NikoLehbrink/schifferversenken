import copy
import random
import time
from Battleship import Battleship
from Gameboard import Gameboard
from Player import Player


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


# event is type, metadata(player,...)
def announce(event_type, metadata={}):
  if event_type == "win":
    print("%s gewinnt! Glückwunsch! " % metadata["player"])
  elif event_type == "new_turn":
    print("%s ist am Zug!" % metadata["player"])
  elif event_type == "hit":
    print("Wow, %s hat ein Schiff getroffen!" % metadata["player"])
  elif event_type == "destroyed":
    print("BOOOM, %s hat das Schiff versenkt!" % metadata["player"])
  elif event_type == "miss":
    print("Leider nicht getroffen, %s!" % metadata["player"])



def get_random_ai_shot(game_board):
  x = random.randint(0, game_board.width - 1 )
  y = random.randint(0, game_board.height - 1)
  return (x,y)

def random_sleepy_ai(sleep_time):
  def function(game_board):
    time.sleep(sleep_time)
    return get_random_ai_shot(game_board)
  return function

def get_human_shot(game_board):
  inp = input("Wo willst du hinschiessen?\n")
  x_str, y_str = inp.split(",")
  x = int(x_str)
  y = int(y_str)
  return (x,y)


def create_random_battleships():
  ship_member = 2
  first_three_long_ship = False
  random_battleships = []

  for i in range(0,5):
    directionList = ["N","E","S","W"]
    # convert to set for intersection method
    directionSet = set(directionList)

    x = random.randint(0, 9)
    y = random.randint(0, 9)
    print("X = %s" %x)
    print("Y = %s" %y)


    if (x + ship_member > 9):
      directionSet = directionSet.intersection(["N","S","W"])
      print("No east")
    if (x - ship_member < 0):
      directionSet = directionSet.intersection(["N","E","S"])
      print("No west")
    if (y + ship_member > 9):
      directionSet = directionSet.intersection(["N","E","W"])

      print("No south")
    if (y - ship_member < 0):
      directionSet = directionSet.intersection(["W","E","S"])
      print("No North")
    print(directionSet)

    # convert back to list for random choice method
    direction = random.choice(list(directionSet))
    new_battleship = Battleship.build((x,y), ship_member, direction)
    random_battleships.append(new_battleship)
    if i == 1 and not first_three_long_ship:
      first_three_long_ship = True
    else:
      ship_member += 1

    print(random_battleships[i].body)
  return random_battleships
    





def run():

  battleships = [
    Battleship.build((1,0), 3, "S"),
    Battleship.build((3,4), 4, "N")
    # Battleship.build((5,7), 3, "E")
  ]

  game_boards = [
    Gameboard(10,10,create_random_battleships()),  
    Gameboard(10,10,copy.deepcopy(battleships))  
  ]

  players = [
    Player("Rob", random_sleepy_ai(2.5)),
    Player("Niko", random_sleepy_ai(2.5))
  ]
  offensive_index = 0

  while(True):
    # Immer die Zahl, die der Gegenpart nicht ist
    defensive_index = (offensive_index + 1) % 2

    defensive_board = game_boards[defensive_index]
    offensive_player = players[offensive_index]

    # print("%s Yoour Turn!" % offensive_player.name)
    announce("new_turn", {"player": offensive_player.name})


    shot_location = offensive_player.shot_function(defensive_board)
    # ToDo: Bad user input

    hit_battleship = defensive_board.take_shot(shot_location)


    render(defensive_board, True)

    if defensive_board.is_game_over():
      announce("win", {"player": offensive_player.name})
      # print("%s You Win" % offensive_player.name)
      break
    
    if hit_battleship is None:
      announce("miss", {"player": offensive_player.name})
      offensive_index = defensive_index
    else:
      if hit_battleship.is_destroyed():
        announce("destroyed", {"player": offensive_player.name})
      else:
        announce("hit", {"player": offensive_player.name})


if __name__=="__main__":
  run()

