from models import message_pb2
from devices.base_device import Device
from devices import colors


class LuzArtificial(Device):
  def __init__(self):
    super().__init__(device_type=message_pb2.ARTIFICIAL_LIGHT)
    self.powered_on = True
    self.intensity = 8  # 0 - 10
    self.color = "light-blue"

  def handle_message(self, message):
    if message.type == message_pb2.TURN_ON:
      self.powered_on = True
      print("Luz artificial: ligado")
    elif message.type == message_pb2.TURN_OFF:
      self.powered_on = False
      print("Luz artificial: desligado")
    elif message.type == message_pb2.CHANGE_COLOR:
      self.color = colors[message.params[0]]
      print(f"Luz artificial: cor mudada para ({self.color})")
    elif message.type == message_pb2.CHANGE_INTENSITY:
      self.intensity = max(min(message.params[0], 10), 0)
      print(f"Luz artificial: intensidade mudada para {self.intensity}")

  def send_status(self):
    pass
