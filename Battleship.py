class Battleship(object):

  @staticmethod
  def build(head, length, direction, name):
    # body ist noch leer
    body = []
    for i in range(length):

      # Z.b.: Wenn direction Nord ist, bleib die x-Koordinate gleich, aber die y-Koordinate ändert sich um die Anzahl der Länge und das neue Element (Touple) wird immer dem Body hinzugefügt
      if direction == "N":
        # head[0] ist x-Koordinate des Schiffbeginns und head[1] ist die y-koordinate 
        element = (head[0], head[1] - i)
      elif direction == "O":
        element = (head[0] + i, head[1])
      elif direction == "S":
        element = (head[0], head[1] + i)
      elif direction == "W":
        element = (head[0] - i, head[1])
      
      body.append(element)
      
    return Battleship(body, head, length, direction, name)

  def __init__(self, body, head, length, direction, name):
    self.body = body
    self.head = head
    self.length = length
    self.direction = direction
    self.hits = [False] * len(body)
    self.name = name
    
  def body_index(self, location):
    try:
      # gibt den Index der Stelle aus, wo im Body die übergebene Location zu finden ist
      return self.body.index(location)
    # Wenn der Wert nicht im Body existiert, dann "None"
    except ValueError:
      return None
  
  def is_destroyed(self):
    for hit in self.hits:
      # sobald auch nur ein hit "False" ist, return false, weil das Schiff nicht zerstört sein kann
      if(hit == False):
        return False
    return True