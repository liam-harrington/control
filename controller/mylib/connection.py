from .default import Default
from .controller import Controller
from .check import Check

from json import dumps
from json import loads

def package(data):
  return dumps(data).encode()

def unpackage(data):
  return loads(data.decode("utf-8"))

class Connection():
  connections = list()
  print("Connection created")
  
  def handle(self):
    from time import sleep
    while self.handling:
      sleep(self.interval)
      if self.updated.is_set():
        result = self.exchange(Controller.data)
        print("Connection.handle:", result)
        for key, value in result.items():
          if value == 'OK':
            del Controller.data[key]
        self.updated.clear()
    self.s.close()
  
  def __init__(self, settings):
    import socket
    import threading
    
    self.handling = True
    
    self.interval = settings.get('send_interval', Default.SEND_INTERVAL)
    
    self.updated = threading.Event()
    
    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    host = settings.get('host', Default.HOST)
    port = settings.get('port', Default.PORT)
    self.s.connect((host, port))
    
    self.thread = threading.Thread(target=self.handle)
    
    Connection.connections.append(self)

    self.checker = Check(self, settings)

  def update(self):
    self.updated.set()
 
  def send(self, data):
    self.s.sendall(package(data))
    
  def recieve(self):
    response, server = self.s.recvfrom(1024)
    if response == b'':
      print("Connection.handle:", response)
      self.handling = False
    else:
      return unpackage(response)
    
  def exchange(self, data):
    self.send(data)
    return self.recieve()
