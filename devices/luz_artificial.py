from models import message_pb2
from base_device import Device


class LuzArtificial(Device):
  def __init__(self):
    super().__init__(device_type=message_pb2.ARTIFICIAL_LIGHT)
    self.powered_on = True
    self.intensity = 8  # 0 - 10
    self.color = (200, 200, 200)

  def handle_message(self, message):
    if message.type == message_pb2.TURN_ON:
      self.powered_on = True
      print("Luz artificial: ligado")
    elif message.type == message_pb2.TURN_OFF:
      self.powered_on = False
      print("Luz artificial: desligado")
    elif message.type == message_pb2.CHANGE_COLOR:
      self.color = (
        max(min(message.params[0], 255), 0),
        max(min(message.params[1], 255), 0),
        max(min(message.params[2], 255), 0),
      )
      print(
        f"Luz artificial: cor mudada para ({self.color[0]},{self.color[1]},{self.color[2]})"
      )
    elif message.type == message_pb2.CHANGE_INTENSITY:
      self.intensity = max(min(message.params[0], 10), 0)
      print(f"Luz artificial: intensidade mudada para {self.intensity}")

  def send_status(self):
    pass
