import socket
import struct
import time
from threading import Thread
from models import message_pb2
from abc import ABC, abstractmethod


class Device(ABC):
  def __init__(
    self,
    device_type,
    multicast_group_ip="224.1.1.1",
    multicast_group_port=5005,
    tcp_listen_ip="0.0.0.0",
    tcp_listen_port=5006,
    gateway_port=5008,
    # precisa ser um ENUM equivalente a algum definido no message.proto
  ):
    self.type = device_type
    self.multicast_group_ip = multicast_group_ip
    self.multicast_group_port = multicast_group_port
    self.tcp_listen_ip = tcp_listen_ip
    self.tcp_listen_port = tcp_listen_port
    self.gateway_ip = None
    self.gateway_port = gateway_port

  @abstractmethod
  def handle_message(self, message):
    """Método abstrato para lidar com mensagens recebidas."""
    pass

  def __send_socket(self, message: bytes, ip_address=None, port=None):
    ip_address = ip_address or self.gateway_ip
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

    forwarded_message = message_pb2.ForwardedMessage()
    forwarded_message.id = 0
    forwarded_message.content.type = message_pb2.REGISTER_DEVICE
    forwarded_message.content.params.append(self.type)

    serialized_auth_message = forwarded_message.SerializeToString()
    self.__send_socket(serialized_auth_message)

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
          message = message_pb2.Message()
          message.ParseFromString(data)
          self.handle_message(message)  # Chama o método abstrato

        gateway_socket.close()
    finally:
      device_socket.close()

  def discover_and_listen(self):
    self.__discover_gateway()
    self.__listen_messages()

  @abstractmethod
  def send_status(self):
    """Método abstrato para enviar informações sobre o status do dispositivo."""
    pass

  def start(self):
    sender_thread_is_started = False

    listen_messages_thread = Thread(target=self.discover_and_listen, daemon=True)
    send_status_thread = Thread(target=self.send_status, daemon=True)

    listen_messages_thread.start()
    print("Thread de escuta iniciada")

    try:
      while True:
        time.sleep(1)
        if self.gateway_ip is not None and not sender_thread_is_started:
          send_status_thread.start()
          print("Thread 2 iniciada")
          sender_thread_is_started = True
    except KeyboardInterrupt:
      print("\nEncerrando o dispositivo.")
