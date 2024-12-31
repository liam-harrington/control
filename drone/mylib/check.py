from .default import Default

class Check():
  print("Check created")
  
  def handle(self):
    from time import sleep
    from time import time
    
    last_time = time()
    
    while self.handling:
      sleep(self.interval)
      if self.connection.updated.is_set():
        last_time = time()
        self.connection.updated.clear()
        print("Check.handle:", self)
      else:
        if (time() - last_time) > self.timeout:
          self.action.disconnect()
          sleep(self.post_disconnect)
  
  def __init__(self, settings, connection, action):
    import threading
    
    self.connection = connection
    self.action = action
    
    self.handling = True
    
    self.timeout = settings.data.get('timeout', 0.5)
    self.interval = settings.data.get('interval', 0.1)
    self.post_disconnect = settings.data.get('post_disconnect', 1.0)
    
    self.thread = self.thread = threading.Thread(target=self.handle)

      

