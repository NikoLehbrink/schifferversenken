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
    print(self.hits)
    for ht in self.hits:
      if(ht == False):
        return False
    return True