def modify(_input, value):
  if _input.get('invert', False):
    value = _input.get('min', 0) + _input.get('max', 1) - value
      
  value *= _input.get('multiply', 1)
              
  value += _input.get('offset', 0)

  return value

class Action():
  print("Action created")
  def __init__(self, settings, connection):
    self.settings = settings
    self.connection = connection
    self.connection.action = self
    self.settings_inputs = self.settings.data.get('inputs', list())
    
  def apply(self, data):
    result = dict()
    for input_code, value in data.items():
      for settings_input in self.settings_inputs:
        if input_code == settings_input.get('code', None):
          value = modify(settings_input, value)
      result[input_code] = 'OK'
    return result
    
  def disconnect(self):
    print("Action.disconnect")
