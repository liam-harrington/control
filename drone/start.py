from mylib import Default
from mylib import Connection
from mylib import Check
from mylib import Settings
from mylib import Action

if __name__ == "__main__":
  settings = Settings()
  settings.load(Default.SETTINGS_PATH)
  
  connection = Connection(settings)
  
  action = Action(settings, connection)
  
  checker = Check(settings, connection, action)
  checker.thread.start()
  
  for connection in Connection.connections:
    connection.thread.start()
