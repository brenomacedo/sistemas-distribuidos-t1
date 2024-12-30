import time
import random
from models import message_pb2
from devices.base_device import Device


class ArCondicionado(Device):
  def __init__(self):
    super().__init__(device_type=message_pb2.AIR_CONDITIONING)
    self.temperature = 25
    self.powered_on = True

  def handle_message(self, message):
    if message.type == message_pb2.TURN_ON:
      self.powered_on = True
      print("Ar condicionado: ligado")
    elif message.type == message_pb2.TURN_OFF:
      self.powered_on = False
      print("Ar condicionado: desligado")
    elif message.type == message_pb2.CHANGE_TEMPERATURE:
      self.temperature = message.params[0]
      print(f"Ar condicionado: temperatura mudada para {message.params[0]}")

  def send_status(self):
    try:
      while True:
        if self.powered_on:
          new_temperature = random.randrange(self.temperature - 1, self.temperature + 1)
          message = message_pb2.ForwardedMessage()
          message.id = 0
          message.content.type = message_pb2.TEMPERATURE_INFO
          message.content.params.append(new_temperature)
          serialized_message = message.SerializeToString()

          self.__send_socket(serialized_message)
          time.sleep(2)
    except Exception as e:
      print(e)
      print("Erro ao tentar enviar informacoes sobre a temperatura do ar condicionado.")
