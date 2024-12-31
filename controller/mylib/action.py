from .controller import Controller

def modify(_input, value):
  if _input.get('invert', False):
    value = _input.get('min', 0) + _input.get('max', 1) - value
      
  value *= _input.get('multiply', 1)
              
  value += _input.get('offset', 0)

  return value

class Action():
  print("Action created")
  def __init__(self, connection):
    self.connection = connection
    
  def apply(self, inputs, event):
    for _input in inputs:
      if _input.get('code', None) == event.code:
        print("Action.apply:", Controller.data)
        Controller.data[_input.get('name', None)] = modify(_input, event.state)
        self.connection.update()
