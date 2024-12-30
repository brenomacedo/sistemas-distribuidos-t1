from models import message_pb2
from devices.base_device import Device
from devices import musics


class CaixaDeSom(Device):
  def __init__(self):
    super().__init__(device_type=message_pb2.SOUND_BOX)
    self.powered_on = False
    self.volume = 30  # 0 - 100
    self.bluetooth_mode = False
    self.music = "lofi"

  def handle_message(self, message):
    if message.type == message_pb2.TURN_ON:
      self.powered_on = True
      print("Caixa de Som: ligado")
    elif message.type == message_pb2.TURN_OFF:
      self.powered_on = False
      print("Caixa de Som: desligado")
    elif message.type == message_pb2.CHANGE_VOLUME:
      self.volume = max(min(message.params[0], 100), 0)
      print(f"Caixa de Som: volume mudado para {self.volume}")
    elif message.type == message_pb2.TURN_ON_BLUETOOTH:
      self.bluetooth_mode = True
      print("Caixa de Som: modo bluetooth ligado")
    elif message.type == message_pb2.TURN_OFF_BLUETOOTH:
      self.bluetooth_mode = False
      print("Caixa de Som: modo bluetooth desligado")
    elif message.type == message_pb2.CHANGE_MUSIC:
      self.music = musics[message.params[0]]
      self.powered_on = True
      print(f"Caixa de Som: musica mudada para {self.music}")

  def send_status(self):
    pass
