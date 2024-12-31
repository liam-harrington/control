class DeviceNotFound(Exception):
  pass

class Controller():
  controllers = list()
  data = dict()
  settings = dict()
  print("Controller created")
  
  def show():
    from inputs import devices
    for id, device in enumerate(devices):
      print(id, device)
  
  def get(device_name):
    from inputs import devices
    for device in devices:
      if str(device) == device_name:
        return device
    raise DeviceNotFound("Could not find Device:", device_name)
  
  def __init__(self, settings, action):
    import threading
    Controller.controllers.append(self)
    self.settings = settings
    self.device = Controller.get(settings['name'])
    self.action = action
    self.thread = threading.Thread(target=self.handle)
    self.handling = True
    
  def handle(self):
    inputs = self.settings.get('inputs', list())
    while self.handling:
      for event in self.device.read():
        if Controller.settings.get('show_events', True):
          print("Controller.handle:", event.code, event.state)
        self.action.apply(inputs, event)

