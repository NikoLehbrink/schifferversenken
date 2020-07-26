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
      # Durch enmuerate macht man names_counter variable und wenn anfang oder ende des schiffes → mach andere zeichen
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

def announce(event_type, metadata={}):
  if event_type == "win":
    print("%s gewinnt! Glückwunsch! " % metadata["player"])
  elif event_type == "new_turn":
    print("%s ist am Zug!" % metadata["player"])
  elif event_type == "hit":
    print("Wow, {0} hat das Schiff {1} getroffen!".format(metadata["player"], metadata["ship_name"]))
  elif event_type == "destroyed":
    print("Booom, {0} hat das Schiff {1} versenkt!".format(metadata["player"], metadata["ship_name"]))
  elif event_type == "miss":
    print("Leider nicht getroffen, %s!" % metadata["player"])
  elif event_type == "wrong_number":
    print("Bitte eine gültige Zahl zwischen 0 und 9 eingeben")
  elif event_type == "wrong_direction":
    print("Invalide Himmelsrichtung!")
  elif event_type == "ship_already_exists":
    print("An dieser Stelle gibt es schon ein Schiff!")
    print("Platziere das Schiff erneut!")
  elif event_type == "out_of_border":
    print("Außerhalb des Wassers dürfen keine Schiffe platziert werden!")
    print("Richtung: %s" % metadata["direction"])
  elif event_type == "collision":
    print("Kollision von {0} mit {1}!".format(metadata["coordinates"], metadata["already_build_battleships"]))
  elif event_type == "ship_placed":
    print("{0} wurde erfolgreich platziert! Koordinaten: {1}".format(metadata["ship_name"], metadata["coordinates"]))
  elif event_type == "invalid_name":
    print("Bitte gib einen Namen ein, der aus Buchstaben besteht!")

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

def is_collision_with_battleship(random_battleships, new_battleship):
  for already_build_battleship in random_battleships:
    for coordinates in already_build_battleship.body:
      if coordinates in new_battleship.body:
        announce("collision", {"coordinates": coordinates,"already_build_battleships": already_build_battleship.body})
        return True
  return False

def is_collision_with_coordinates(random_battleships, coords):
  for already_build_battleship in random_battleships:
    for coordinates in already_build_battleship.body:
      if coordinates == coords:
        announce("collision", {"coordinates": coords,"already_build_battleships": already_build_battleship.body})
        return True
  return False

def create_own_battleships():
  ship_length = 2
  first_ship_with_length_three = False
  battleships = []
  names = ["Destroyer", "Submarine", "Cruiser", "Battleship", "Carrier"]
  name_counter = 0
  directionList = ['N','E','S','W']

  while(ship_length <= 5):
    while(True):
      try:
        x = int(input("In welcher Spalte soll das Schiff platziert werden?\n"))
        if not(0 <= x <= 9):
          announce("wrong_number")
          continue
        y = int(input("In welcher Zeile soll das Schiff platziert werden?\n"))
        if not(0 <= y <= 9):
          announce("wrong_number")
          continue
        coords = (x,y)
        if is_collision_with_coordinates(battleships, coords):
          announce("ship_already_exists")
        else:
          break
      except ValueError:
        announce("wrong_number")
      
    while(True):
      print("In welche Himmelsrichtung soll dein Schiff zeigen?")
      direction = input("Eingabe: 'N','E', 'S', 'W'\n").upper()

      if not direction in directionList:
        announce("wrong_direction")
        continue

      if (x + ship_length - 1 > 9 and direction == 'E'):
        announce("out_of_border", {"direction": direction})
        continue
      if (x - ship_length + 1 < 0 and direction == 'W'):
        announce("out_of_border", {"direction": direction})
        continue
      if (y + ship_length - 1 > 9 and direction == 'S'):
        announce("out_of_border", {"direction": direction})
        continue
      if (y - ship_length + 1 < 0 and direction == 'N'):
        announce("out_of_border", {"direction": direction})
        continue

      new_battleship = Battleship.build((x,y), ship_length, direction, names[name_counter])

      if is_collision_with_battleship(battleships, new_battleship):
        announce("ship_already_exists")
        break
      else:
        battleships.append(new_battleship)
        announce("ship_placed", {"ship_name": new_battleship.name, "coordinates": new_battleship.body})

      if ship_length == 3 and not first_ship_with_length_three:
        first_ship_with_length_three = True
      else:
        ship_length += 1
      name_counter += 1 
      break
    
    # for r in battleships:
    #   print("Alle Schiffe: %s" %r.body)

  return battleships
  


def create_random_battleships():
  ship_length = 2
  first_ship_with_length_three = False
  random_battleships = []
  names = ["Destroyer", "Submarine", "Cruiser", "Battleship", "Carrier"]
  names_counter = 0

  while(ship_length <= 5):
    directionList = ["N","E","S","W"]
    # convert to set for intersection method
    directionSet = set(directionList)
    x = random.randint(0, 9)
    y = random.randint(0, 9)
    coords = (x,y)

    # print("x = {0}, y = {1}".format(x,y))

    if not is_collision_with_coordinates(random_battleships, coords):

      if (x + ship_length - 1 > 9):
        directionSet = directionSet.intersection(["N","S","W"])
      if (x - ship_length + 1 < 0):
        directionSet = directionSet.intersection(["N","E","S"])
      if (y + ship_length - 1 > 9):
        directionSet = directionSet.intersection(["N","E","W"])
      if (y - ship_length + 1 < 0):
        directionSet = directionSet.intersection(["W","E","S"])
      # print("Mögliche Richtungen: {0}".format(directionSet))

      # convert back to list for random choice method
      direction = random.choice(list(directionSet))
      new_battleship = Battleship.build((x,y), ship_length, direction, names[names_counter])

      if not is_collision_with_battleship(random_battleships, new_battleship):
        random_battleships.append(new_battleship)
        announce("ship_placed", {"ship_name": new_battleship.name, "coordinates": new_battleship.body})

        # Weil es zwei Schiffe mit einer Länge von 3 gibt
        if ship_length == 3 and not first_ship_with_length_three:
          first_ship_with_length_three = True
        else:
          ship_length += 1
        names_counter += 1
      else:
        del(new_battleship)
      
  # for r in random_battleships:
  #   print("%s ist auf %s positioniert!" %(r.name, r.body))
      
  return random_battleships
    

def run():
  players = []
  game_boards = []

  for i in range(1,3):
    while(True):
      name = input("Spieler %s: Bitte Namen eingeben: " %i)
      if not "".join(name.split()).isalpha():
        announce("invalid_name")
        continue
      break
    while(True):
      print("Welcher Spielertyp soll %s sein?" %name)
      player_type = input("'C' für Computer generiert, 'M' für Mensch: ").lower()
      if player_type == 'c':
        player = Player(name, random_sleepy_ai(1))
        gameboard = Gameboard(10,10,create_random_battleships())  
        players.append(player)
        game_boards.append(gameboard)
        break
      elif player_type == 'm':
        player = Player(name, get_human_shot)
        gameboard = Gameboard(10,10,create_own_battleships())  
        players.append(player)
        game_boards.append(gameboard)
        break
      else:
        print("gib richtige string ein")
        continue
  



      


  # game_boards = [
  #   Gameboard(10,10,create_random_battleships()),  
  #   Gameboard(10,10,create_own_battleships())  
  # ]

  # players = [
  #   Player("Rob", get_human_shot),
  #   Player("Niko", random_sleepy_ai(2.5))
  # ]
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
      print(hit_battleship.name)
      if hit_battleship.is_destroyed():
        announce("destroyed", {"player": offensive_player.name, "ship_name": hit_battleship.name})
      else:
        announce("hit", {"player": offensive_player.name, "ship_name": hit_battleship.name})


if __name__=="__main__":
  run()