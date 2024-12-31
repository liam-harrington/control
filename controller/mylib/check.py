from .default import Default

class Check():
  print("Check created")

  def handle(self):
    from time import sleep
    timeout_package = {'timeout': False}
    
    
    
    while True:
      sleep(self.interval)
      response = self.connection.exchange(timeout_package)
      print("Check.handle:", response)
      
      
  
  def __init__(self, connection, settings):
    import threading
    
    self.interval = settings.get('interval', Default.CHECK_INTERVAL)
    
    self.connection = connection
    self.thread = threading.Thread(target=self.handle)
