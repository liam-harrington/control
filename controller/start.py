from mylib import Default
from mylib import Connection
from mylib import Controller
from mylib import Check
from mylib import Action
from mylib import Settings



if __name__ == "__main__":
  settings = Settings()
  settings.load(Default.SETTINGS_PATH)
  
  connection = Connection(settings.data)
  connection.data = {'test': True}
  connection.update()
  
  action = Action(connection)
  
  if settings.data.get('show_devices', True):
    Controller.show()
  
  for device_settings in settings.data['devices']:
    controller = Controller(device_settings, action)
    
  for controller in Controller.controllers:
    controller.thread.start()
    
  for connection in Connection.connections:
    connection.thread.start()
    connection.checker.thread.start()
