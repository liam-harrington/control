from .default import Default

from json import dumps
from json import loads

def package(data):
  return dumps(data).encode()

def unpackage(data):
  return loads(data.decode("utf-8"))
  
def modify(_input, value):
  if _input.get('invert', False):
    value = _input.get('min', 0) + _input.get('max', 1) - value
      
  value *= _input.get('multiply', 1)
              
  value += _input.get('offset', 0)

  return value

class Client():
  print("Client created")
  def __init__(self, connection, action, socket_connection, addr):
    import threading

    self.connection = connection
    self.action = action
    
    self.socket_connection = socket_connection
    self.addr = addr
    
    self.handling = True
    
    self.thread = threading.Thread(target=self.handle)
    
    print(f"Connected by {addr}")
    
    
  def handle(self):
    while self.handling:
      data = self.connection.recieve(self)
      self.connection.updated.set()
      result = self.action.apply(data)
      self.connection.send(self.socket_connection, result)
      #print("Client.handle data:", self.connection.data)
      print("Client.handle result:", result)
    self.socket_connection.close()

class Connection():
  print("Connection created")
  connections = list()
  
  def handle(self):
    while self.handling:
      print("Connection.handle")
      socket_connection, addr = self.s.accept()
      client = Client(self, self.action, socket_connection, addr)
      client.thread.start()
  
  def __init__(self, settings):
    import socket
    import threading
    
    Connection.connections.append(self)
    
    self.action = None
    self.handling = True
    self.data = dict()
    
    self.updated = threading.Event()
    
    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.s.bind((settings.data.get('host', Default.HOST), settings.data.get('port', Default.PORT)))
    self.s.listen()
    
    self.thread = threading.Thread(target=self.handle)
    
  def send(self, connection, data):
    connection.sendall(package(data))
    
  def recieve(self, client):
    response, server = client.socket_connection.recvfrom(1024)
    print("Connection.handle:", response)
    if response == b'':
      client.handling = False
      return {}
    else:
      return unpackage(response)
