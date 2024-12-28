from models import message_pb2
from base_device import Device


class Porta(Device):
  def __init__(self):
    super().__init__(device_type=message_pb2.DOOR)
    self.locked = False

  def handle_message(self, message):
    if message.type == message_pb2.LOCK:
      self.powered_on = True
      print("Porta: trancada")
    elif message.type == message_pb2.UNLOCK:
      self.powered_on = False
      print("Porta: destrancada")

  def send_status(self):
    pass
