from .default import Default

class Settings():
  print("Settings created")
  
  def __init__(self):
    self.data = None

      
  def load(self, path):
    import yaml
    try:
      self.stream = open(path)
    except FileNotFoundError as exc:
      print("Please create a drone.yaml file", exc)
    try:
      self.data = yaml.safe_load(self.stream)
    except yaml.YAMLError as exc:
      print("Please fix youre YAML error", exc)
    self.stream.close()
