from models import message_pb2
from base_device import Device


class Televisao(Device):
  def __init__(self):
    super().__init__(device_type=message_pb2.TELEVISION)
    self.powered_on = True
    self.volume = 30  # 0 - 100
    self.channel = 10
    self.led_volume_sync = False

  def handle_message(self, message):
    if message.type == message_pb2.TURN_ON:
      self.powered_on = True
      print("Televisao: ligado")
    elif message.type == message_pb2.TURN_OFF:
      self.powered_on = False
      print("Televisao: desligado")
    elif message.type == message_pb2.CHANGE_VOLUME:
      self.volume = max(min(message.params[0], 100), 0)
      print(f"Televisao: volume mudado para {self.volume}")
    elif message.type == message_pb2.CHANGE_CHANNEL:
      self.channel = max(message.params[0], 0)
      print(f"Televisao: canal mudado para {self.channel}")
    elif message.type == message_pb2.TURN_ON_LED_VOLUME_SYNC:
      self.led_volume_sync = True
      print("Televisao: modo sincronizar volume com led ligado")
    elif message.type == message_pb2.TURN_OFF_LED_VOLUME_SYNC:
      self.led_volume_sync = False
      print("Televisao: modo sincronizar volume com led desligado")

  def send_status(self):
    pass
