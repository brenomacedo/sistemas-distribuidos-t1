import socket
import struct
import time
import random
from models import message_pb2
from threading import Thread


class ArCondicionado:
  gateway_ip: str  # | None = None

  def __init__(
    self,
    multicast_group_ip: str = "224.1.1.1",
    multicast_group_port: int = 5005,
    tcp_listen_ip: str = "0.0.0.0",
    tcp_listen_port: int = 5006,
    gateway_port: str = 5008,
  ):
    self.multicast_group_ip = multicast_group_ip
    self.multicast_group_port = multicast_group_port
    self.tcp_listen_ip = tcp_listen_ip
    self.tcp_listen_port = tcp_listen_port
    self.gateway_ip = None
    self.gateway_port = gateway_port

  def __send_socket(self, message: bytes, ip_address=None, port=None):
    ip_address: str = ip_address or self.gateway_ip
    port = port or self.gateway_port

    if ip_address is None:
      return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip_address, port))

    client_socket.sendall(message)
    client_socket.close()

  def __discover_gateway(self):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", self.multicast_group_port))

    group = socket.inet_aton(self.multicast_group_ip)
    mreq = struct.pack("4sL", group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    data, address = sock.recvfrom(1024)
    self.gateway_ip = address[0]
    print("GATEWAY IP SETADO:", self.gateway_ip)
    print(f"Mensagem recebida do gateway {address}")

    message = message_pb2.Message()
    message.ParseFromString(data)
    sock.close()

    # Substituir aqui a mensagem por uma codificacao de protobuff
    # das informacoes do device'
    message.type = message_pb2.REGISTER_DEVICE
    param = message.params.add()
    param.type = message_pb2.DEVICE_TYPE
    param.value = message_pb2.AIR_CONDITIONING
    serialized_message = message.SerializeToString()
    self.__send_socket(serialized_message)

  def __listen_messages(self):
    device_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    device_socket.bind((self.tcp_listen_ip, self.tcp_listen_port))
    device_socket.listen(10)

    try:
      while True:
        gateway_socket, gateway_address = device_socket.accept()
        print(f"Conexão estabelecida com {gateway_address}")

        data = gateway_socket.recv(1024)
        if data:
          chat_message = message_pb2.ChatMessage()
          chat_message.ParseFromString(data)
          print(f"Mensagem recebida de {chat_message.sender}: {chat_message.message}")

          # decoded_data = data.decode("utf-8")
          # print(f"Dado recebido do gateway: {decoded_data}")

          # IF DATA.TIPO == MUDAR_TEMPERATURA, MUDAR A TEMPERATURA DO AR CONDICIONADO

        gateway_socket.close()
    finally:
      device_socket.close()

  def discover_and_listen(self):
    self.__discover_gateway()
    self.__listen_messages()

  def send_temperature(self):
    try:
      while True:
        message = (
          "Temperatura nova do ar condicionado: "
          + str(random.randrange(18, 26))
          + " graus celsius"
        )
        self.__send_socket(message.encode("utf-8"))
        time.sleep(2)
    except Exception:
      print("Erro ao tentar enviar informacoes sobre a temperatura do ar condicionado.")

  def start(self):
    sender_thread_is_started = False

    # Iniciar threads para envio e recepção
    listen_messages_thread = Thread(target=self.discover_and_listen, daemon=True)
    send_temperature_thread = Thread(target=self.send_temperature, daemon=True)

    listen_messages_thread.start()
    print("Thread 1 iniciada")
    # send_temperature_thread.start()

    try:
      while True:
        time.sleep(1)
        if self.gateway_ip is None and not sender_thread_is_started:
          send_temperature_thread.start()
          print("Thread 2 iniciada")
          sender_thread_is_started = True
    except KeyboardInterrupt:
      print("\nEncerrando o gateway.")
