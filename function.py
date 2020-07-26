

def create_random_battleships():
  ship_member = 2
  first_three_long_ship = False
  random_battleships = []
  prevBattleships = []

  while(ship_member <= 5):
    directionList = ["N","E","S","W"]
    # convert to set for intersection method
    directionSet = set(directionList)

    x = random.randint(0, 9)
    y = random.randint(0, 9)
    coords = (x,y)
    print("X = {0}, Y = {1}".format(x,y))

    if (coords) not in prevBattleships:
      print(" ${0} GIBTS NOCH NICHT".format(coords))
      # print(prevBattleships)

      if (x + ship_member > 9):
        directionSet = directionSet.intersection(["N","S","W"])
        # print("No east")
      if (x - ship_member < 0):
        directionSet = directionSet.intersection(["N","E","S"])
        # print("No west")
      if (y + ship_member > 9):
        directionSet = directionSet.intersection(["N","E","W"])
        # print("No south")
      if (y - ship_member < 0):
        directionSet = directionSet.intersection(["W","E","S"])
        # print("No North")
      print("Possible directions: {0}".format(directionSet))

      # convert back to list for random choice method
      direction = random.choice(list(directionSet))
      new_battleship = Battleship.build((x,y), ship_member, direction)
      print("Neues Battleship: {0}".format(new_battleship.body))

      if not is_collision(random_battleships, new_battleship):
        random_battleships.append(new_battleship)
        if ship_member == 3 and not first_three_long_ship:
          first_three_long_ship = True
        else:
          ship_member += 1
        prevBattleships.append(coords)
      else:
        print("Neuer Versuch")

  for r in random_battleships:
    print("Alle Schiffe: %s" %r.body)
  return random_battleships



def create_own_battleships():
  ship_member = 2
  first_three_long_ship = False
  battleships = []
  prevBattleships = []

  while(ship_member <= 5):
    while(True):
      try:
        x = int(input("In welcher Spalte soll das Schiff platziert werden?"))
        if(0 <= x <= 9):
          print("hi")
        else: 
          print("Bitte eine gültige Zahl zwischen 0 und 9 eingeben")
          continue
        y = int(input("In welcher Zeile soll das Schiff platziert werden?"))
        if(0 <= y >= 9):
          coords = (x,y)
          print(coords)
          break
      except ValueError:
        print("Bitte ein gülitge Zahl eingeben.")
      
    
    print("In welche Himmelsrichtung soll dein Schiff zeigen?")
    direction = input("Möglich: 'N','E', 'S', 'W'")

    coords = (x,y)
    print("X = {0}, Y = {1}".format(x,y))

    if (coords) not in prevBattleships:
      print(" ${0} GIBTS NOCH NICHT".format(coords))
      # print(prevBattleships)

      if (x + ship_member > 9):
        directionSet = directionSet.intersection(["N","S","W"])
        # print("No east")
      if (x - ship_member < 0):
        directionSet = directionSet.intersection(["N","E","S"])
        # print("No west")
      if (y + ship_member > 9):
        directionSet = directionSet.intersection(["N","E","W"])
        # print("No south")
      if (y - ship_member < 0):
        directionSet = directionSet.intersection(["W","E","S"])
        # print("No North")
      print("Possible directions: {0}".format(directionSet))

      # convert back to list for random choice method
      direction = random.choice(list(directionSet))
      new_battleship = Battleship.build((x,y), ship_member, direction)
      print("Neues Battleship: {0}".format(new_battleship.body))

      if not is_collision(random_battleships, new_battleship):
        random_battleships.append(new_battleship)
        if ship_member == 3 and not first_three_long_ship:
          first_three_long_ship = True
        else:
          ship_member += 1
        prevBattleships.append(coords)
      else:
        print("Neuer Versuch")

  for r in random_battleships:
    print("Alle Schiffe: %s" %r.body)
  return battleships
  