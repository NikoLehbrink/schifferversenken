# Niko Lehbrink, HSB, Python 3-Kurs, Endabgabe
import random
import time
import os
from colorama import init, Fore, Back, Style

from Battleship import Battleship
from Gameboard import Gameboard
from Player import Player

# Initialisierung für Colorama, damit Terminal-Zeilen farbig ausgegeben werden können. 
init()

#Render-Funktion zum Anzeigen der Gameboards
def render(game_board, show_battleships=False):

  board = []
  for x in range(game_board.width):
    # Erst einmal überall None setzen, 
    board.append([None for y in range(game_board.height)])

  # Debugging-Funktion - Bei Funktionsaufruf von render() in run(), den zweiten Übergabewert auf True setzen, damit man alle Schiffe während des Spiels sehen kann 
  if(show_battleships):
    for b in game_board.battleships:
      # Durch enmuerate hat man die möglichkeit der Deklarierung einer Counter variable - wenn Anfang oder Ende des Schiffes → macht andere zeichen, als das '+'
      for i,(x,y) in enumerate(b.body):
        if b.direction == "N":
          characters = (" v", " +", " ^")
        if b.direction == "S":
          characters = (" ^", " +", " v")
        if b.direction == "E":
          characters = (" <", " +", " >")
        if b.direction == "W":
          characters = (" >", " +", " <")

        if i == 0:
          character= characters[0]
        elif i == len(b.body) - 1:
          character = characters[2]
        else:
          character = characters[1]
        board[x][y] = character

  # Add shots to the board
  for shot in game_board.shots:
    # Jeweiliger Wert des Touples wird direkt in Variablen gespeichert
    x, y = shot.location
    if shot.is_hit:
      character = Fore.RED + " X" + Style.RESET_ALL
    else:
      character = Fore.CYAN + " »" + Style.RESET_ALL
    board[x][y] = character
  
  # Top-Reihe für Feld
  field_border_top = Fore.LIGHTBLACK_EX + "  0 1 2 3 4 5 6 7 8 9" + Style.RESET_ALL
  print(field_border_top)

  for y in range(game_board.height):
    row = []
    for x in range(game_board.width):
      # Fügt entweder den Charakter dem Board hinzu, oder ' O', wenn Location noch None ist
      row.append(board[x][y] or Fore.LIGHTWHITE_EX + " O" + Style.RESET_ALL)
    print(Fore.LIGHTBLACK_EX + str(y)  + Style.RESET_ALL + "".join(row))
  
# print-Funktion, die es einfacher macht, ausgaben zu tätigen, als immer print(...) zu schreiben
def announce(event_type, metadata={}):
  if event_type == "win":
    print(Fore.GREEN + "%s gewinnt! Glückwunsch!" % metadata["player"] + Style.RESET_ALL)
  elif event_type == "new_turn":
    print("%s ist am Zug!" % metadata["player"])
  elif event_type == "hit":
    print(Fore.LIGHTGREEN_EX + "Wow, {0} hat das Schiff '{1}' getroffen!".format(metadata["player"], metadata["ship_name"]) + Style.RESET_ALL)
  elif event_type == "destroyed":
    print(Fore.GREEN + "Booom!!! {0} hat das Schiff '{1}' versenkt!".format(metadata["player"], metadata["ship_name"]) + Style.RESET_ALL)
  elif event_type == "miss":
    print(Fore.LIGHTRED_EX + "Leider nicht getroffen, %s!" % metadata["player"] + Style.RESET_ALL)
  elif event_type == "wrong_number":
    print(Fore.RED + "Bitte eine gültige Zahl zwischen 0 und 9 eingeben" + Style.RESET_ALL)
  elif event_type == "wrong_direction":
    print(Fore.RED + "Invalide Himmelsrichtung!" + Style.RESET_ALL)
  elif event_type == "place_already_occupied":
    print(Fore.RED + "An dieser Stelle gibt es schon ein Schiff!")
    print("Platziere das Schiff erneut!" + Style.RESET_ALL)
  elif event_type == "out_of_border":
    print(Fore.RED + "Außerhalb des Wassers dürfen keine Schiffe platziert werden!" + Style.RESET_ALL)
  elif event_type == "collision":
    print("Kollision von " + Fore.RED + "{0}".format(metadata["coordinates"]) + Style.RESET_ALL + " mit " + Fore.RED + "{0}".format(metadata["already_build_battleships"]) + Style.RESET_ALL)
  elif event_type == "already_shot":
    print(Fore.MAGENTA + "Auf {0} wurde schon geschossen!".format(metadata["coordinates"]) + Style.RESET_ALL)
  elif event_type == "ship_placed":
    print("{0} wurde erfolgreich platziert! Koordinaten: {1}".format(metadata["ship_name"], metadata["coordinates"]))
  elif event_type == "ship_successfully_placed":
    print(Fore.GREEN + "Alle Schiffe wurden erfolgreich platziert!" + Style.RESET_ALL)
  elif event_type == "invalid_name":
    print("Bitte gib einen Namen ein, der aus Buchstaben besteht!")
  elif event_type == "next_try":
    print(Fore.LIGHTYELLOW_EX + "Du darfst nochmal schiessen" + Style.RESET_ALL)
  elif event_type == "shot_location":
    print("Schuss auf {0}".format(metadata["coordinates"]))
  elif event_type == "no_valid_input":
    print(Fore.RED + "Gib eine valide Eingabe ein!" + Style.RESET_ALL)



# Funktion für zufälligen Schuss,der vom Computer ausgefhürt wird.
def get_random_ai_shot(game_board):
  while (True):   
    x = random.randint(0, game_board.width - 1 )
    y = random.randint(0, game_board.height - 1)
    coords = (x,y)
    if not already_shot_at(coords, game_board):
      return (x,y)

# Funktion für einen vom Menschen ausgeführten Spielzug
def get_human_shot(game_board):
  while(True):
    try:
      print("")
      print("Wo willst du hinschiessen?")
      x = int(input("Reihe: "))
      if not(0 <= x <= game_board.width - 1):
        announce("wrong_number")
        continue
      y = int(input("Spalte: "))
      if not(0 <= y <= game_board.height - 1):
        announce("wrong_number")
        continue
      if already_shot_at((x,y), game_board):
        continue
      else:
        break
    except ValueError:
      announce("wrong_number")
  return (x,y)

# Funktion: Wenn die Head-Koordinate mit einem anderen Schiff kollidiert 
def is_collision_with_coordinates(random_battleships, coords):
  for already_build_battleship in random_battleships:
    for coordinates in already_build_battleship.body:
      if coordinates == coords:
        # debugging-ausgabe, mit welchem Schiff kollidiert wird
        # announce("collision", {"coordinates": coords,"already_build_battleships": already_build_battleship.name})
        return True
  return False

# Funktion: Wenn die Head-Koordinate nicht mit einem anderem Schiff kollidiert, aber der daraufhin berechnete Rumpf des neuen Schiffs mit einem vorhandenen Schiff kollidiert
def is_collision_with_battleship(random_battleships, new_battleship):
  for already_build_battleship in random_battleships:
    for coordinates in already_build_battleship.body:
      if coordinates in new_battleship.body:
        # debugging-ausgabe, mit welchem Schiff kollidiert wird
        # announce("collision", {"coordinates": coordinates,"already_build_battleships": already_build_battleship.name})
        return True
  return False

# Funktion: Wenn schon auf diese Koordinate geschossen wurde
def already_shot_at(coords, game_board):
  for shot in game_board.shots: 
    if shot.location == coords:
      announce("already_shot",{"coordinates": coords})
      return True
  return False

# Funktion zum Erstellen eigener Schiffe
def create_own_battleships():
  ship_length = 2
  first_ship_with_length_three = False
  battleships = []
  names = ["Destroyer", "Submarine", "Cruiser", "Battleship", "Carrier"]
  name_counter = 0
  directionList = ['N','O','S','W']

  while(ship_length <= 5):
    while(True):
      try:
        x = int(input("In welcher Reihe soll das Schiff '%s' platziert werden?\n" %names[name_counter]))
        if not(0 <= x <= 9):
          announce("wrong_number")
          continue
        y = int(input("In welcher Spalte soll das Schiff platziert werden?\n"))
        if not(0 <= y <= 9):
          announce("wrong_number")
          continue
        coords = (x,y)
        if is_collision_with_coordinates(battleships, coords):
          announce("place_already_occupied")
        else:
          break
      except ValueError:
        announce("wrong_number")
      
    while(True):
      print("In welche Himmelsrichtung soll dein Schiff zeigen?")
      direction = input("Eingabe: 'N','O', 'S', 'W'\n").upper()

      if not direction in directionList:
        announce("wrong_direction")
        continue

      # Berechnung wenn Kooordinaten in Ordnung sind, aber die gewählte Himmelsrichtung, ein Schiff ausserhalb des Feldes bedeuten würde. 
      if y - ship_length + 1 < 0 and direction == 'N' or \
        x + ship_length - 1 > 9 and direction == 'O' or \
        y + ship_length - 1 > 9 and direction == 'S' or \
        x - ship_length + 1 < 0 and direction == 'W':
          announce("out_of_border", {"direction": direction})
          continue
      new_battleship = Battleship.build((x,y), ship_length, direction, names[name_counter])
  
      if is_collision_with_battleship(battleships, new_battleship):
        announce("place_already_occupied")
        break
      else:
        battleships.append(new_battleship)
        announce("ship_placed", {"ship_name": new_battleship.name, "coordinates": new_battleship.body})

      # Weil es zwei Schiffe mit einer Länge von 3 gibt
      if ship_length == 3 and not first_ship_with_length_three:
        first_ship_with_length_three = True
      else:
        ship_length += 1
      name_counter += 1 
      break

  return battleships

def create_random_battleships():
  ship_length = 2
  first_ship_with_length_three = False
  random_battleships = []
  names = ["Destroyer", "Submarine", "Cruiser", "Battleship", "Carrier"]
  names_counter = 0

  while(ship_length <= 5):
    directionList = ["N","O","S","W"]
    # Die Liste wird zu einem Set konvertiert, weil man auf dem Set die intersection-Methode aufrufen kann
    directionSet = set(directionList)
    x = random.randint(0, 9)
    y = random.randint(0, 9)
    coords = (x,y)

    if not is_collision_with_coordinates(random_battleships, coords):
      # Weil eine zufällige Himmelsrichtung ausgewählt werden soll, muss im Vorhinein geprüft werden, welche Himmelsrichtung überhaupt möglich ist, ohne dass das Schiff außerhalb des Spielfeldes platziert wird. Deswegen eine Schnittmengen-Methode, die das directionSet anpasst und nur die möglichen Himmelsrichtungen speichert 
      if (x + ship_length - 1 > 9):
        directionSet = directionSet.intersection(["N","S","W"])
      if (x - ship_length + 1 < 0):
        directionSet = directionSet.intersection(["N","O","S"])
      if (y + ship_length - 1 > 9):
        directionSet = directionSet.intersection(["N","O","W"])
      if (y - ship_length + 1 < 0):
        directionSet = directionSet.intersection(["W","O","S"])

      # Die Liste wird zurückkonvertiert um die random.choice-Methode aufzurufen
      direction = random.choice(list(directionSet))
      # Das neue Schiff wird deklariert, aber noch nicht in der finalen Liste gespeichert
      new_battleship = Battleship.build((x,y), ship_length, direction, names[names_counter])

      if not is_collision_with_battleship(random_battleships, new_battleship):
        random_battleships.append(new_battleship)

        # announce("ship_placed", {"ship_name": new_battleship.name, "coordinates": new_battleship.body})     # Zum Debuggen, wo einzelne Schiffe platziert wurde

        # Weil es zwei Schiffe mit einer Länge von 3 gibt
        if ship_length == 3 and not first_ship_with_length_three:
          first_ship_with_length_three = True
        else:
          ship_length += 1
        names_counter += 1
      else:
        del(new_battleship)
  
  announce("ship_successfully_placed")
      
  return random_battleships
    
# Die Methode zum Starten des Spiels
def run():
  players = []
  game_boards = []

  print("""
  Willkommen zu Niko Lehbrink's Schiffe Versenken!
  Nachdem du deinen Spielern Namen gegeben hast, 
  kannst du auswählen, ob dieser Computergeneriert wird,
  oder ob eine reale Person dahinter steckt...

  Die Regeln: 
  Es gibt 5 Boote, die zu verteilen sind oder automatisch verteilt werden.
  Pro Runde darf man einmal schiessen; sobald ein gegnerisches 
  Schiff getroffen wurde, ist der angreifende Spieler nochmal am Zug.
  Ein Treffer wird als rotes """ + Fore.RED + "X" + Style.RESET_ALL + """ angezeigt.
  Ein missglückter Schuss ins Wasser wird als blaues """ + Fore.CYAN + "»" + Style.RESET_ALL + """ angezeigt.

  Viel Erfolg!

              |    |    |
             )_)  )_)  )_)
            )___))___))___)
           )____)____)_____)
         _____|____|____|____\___
---------\                   /---------
  ^^^^^ ^^^^^^^^^^^^^^^^^^^^^
    ^^^^      ^^^^     ^^^    ^^
         ^^^^      ^^^
  """)

  #  1 bis 3, weil Spielernummer so einfacher ausgegeben wird - statt Spieler 0, wird dadurch Spieler 1 ausgegeben
  for i in range(1,3):
    while(True):
      name = input("Spieler %s: Bitte Namen eingeben: " %i)
      # Wenn Vor und Nachname eingegeben wird und der zusammengefügte String nicht nur Buchstaben enthält
      if not "".join(name.split()).isalpha():
        announce("invalid_name")
        continue
      break
    while(True):
      print("Welcher Spielertyp soll %s sein?" %name)
      player_type = input("'C' für Computergeneriert, 'M' für Mensch: ").lower()
      if player_type == 'c':
        player = Player(name, get_random_ai_shot)
        gameboard = Gameboard(10,10,create_random_battleships())  
        players.append(player)
        game_boards.append(gameboard)
        break
      elif player_type == 'm':
        # Beim Auswählen eines menschlichen Spielers, ist es möglich die Schiffe automatisch zu platzieren, oder dies händisch zu tun
        player = Player(name, get_human_shot)
        # Bei einmaligen Ausgaben und input-Methoden wurde auf die Benutzung der announce-Methode verzichtet
        print("Möchtest du deine Schiffe selbst platzieren?")
        while(True):
          create_ships = input("'J' für selbst generieren, 'N' für Computergeneriert: ").lower()
          if create_ships == 'j':
            gameboard = Gameboard(10,10,create_own_battleships())
            break
          elif create_ships == 'n':
            gameboard = Gameboard(10,10,create_random_battleships())
            time.sleep(3)
            break
          else:
            announce("no_valid_input")
            continue
        players.append(player)
        game_boards.append(gameboard)
        break
      else:
        print("Gib einen validen Spielertypen ein!")
        continue
  
  offensive_index = 0
  time_in_between_turns = 4
  while(True):
    print(Fore.LIGHTYELLOW_EX + "Wie viele Sekunden sollen zwischen den einzelnen Spielzügen gewartet werden?" + Style.RESET_ALL )
    try:
      time_in_between_turns = float(input("Eingabe erfolgt als Zahl (Empf.: 4): "))
    except ValueError:
      announce("no_valid_input")
      continue
    break
  while(True):
    # Clear Terminal
    os.system('cls')
    # Immer die Zahl, die der Gegenpart nicht ist
    defensive_index = (offensive_index + 1) % 2

    defensive_board = game_boards[defensive_index]
    offensive_player = players[offensive_index]
    defensive_player =  players[defensive_index]

    # Zur eindeutigen Benennung, wessen Feld ab der nächsten Line gezeigt wird
    print("%s's Feld:" %defensive_player.name)
    # Wenn auf True gesetzt, dann sieht man alle Schiffe auf dem Spielfeld
    render(defensive_board, False)
    print("")
    announce("new_turn", {"player": offensive_player.name})

    # Welche Koordinaten als nächstes beschossen werden sollen
    shot_location = offensive_player.shot_function(defensive_board)
    # Clear, damit nun das aktualisierte Board mit kommendem Schuss an gleicher Stelle im Terminal angezeigt wird.
    os.system('cls')
    # Schuss auf die vorher ausgewählten Koordinaten
    hit_battleship = defensive_board.take_shot(shot_location)
    print("%s's Feld:" %defensive_player.name)
    # Wenn auf True gesetzt, dann sieht man alle Schiffe auf dem Spielfeld
    render(defensive_board, False)
    print("")
    # Um die Anzeige etwas nutzerfreundlicher zu machen
    if(offensive_player.shot_function.__name__ != "get_human_shot"):
      announce("new_turn", {"player": offensive_player.name})
      print("")

    announce("shot_location",{"coordinates": shot_location})

    if defensive_board.is_game_over():
      announce("win", {"player": offensive_player.name})
      time.sleep(5)
      break
    if hit_battleship is None:
      # Wenn nicht getroffen, switche die Spieler und der nächste Spieler darf jetzt spielen
      announce("miss", {"player": offensive_player.name})
      offensive_index = defensive_index
    else:
      if hit_battleship.is_destroyed():
        announce("destroyed", {"player": offensive_player.name, "ship_name": hit_battleship.name})
      else:
        # Wenn ein Hit, aber nicht zerstört
        announce("hit", {"player": offensive_player.name, "ship_name": hit_battleship.name})
      announce("next_try")
    # Zeit zwischen den einzelnen Spielzügen
    time.sleep(time_in_between_turns)

if __name__=="__main__":
  run()