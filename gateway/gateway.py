import socket
import time
from threading import Thread
from models import message_pb2
from devices import message_types


class Gateway:
  def __init__(
    self,
    multicast_group_ip: str = "224.0.0.1",
    multicast_group_port: int = 5001,
    tcp_listen_ip: str = "0.0.0.0",
    tcp_listen_port: int = 5008,
    devices_port: int = 5006,
    discover_interval_in_seconds: int = 5,
    client_ip: str = "172.31.92.40",
    client_port: int = 5001,
  ):
    self.device_counter = 0
    self.registered_devices = []

    self.multicast_group_ip = multicast_group_ip
    self.multicast_group_port = multicast_group_port
    self.tcp_listen_ip = tcp_listen_ip
    self.tcp_listen_port = tcp_listen_port
    self.devices_port = devices_port
    self.discover_interval_in_seconds = discover_interval_in_seconds
    self.client_ip = client_ip
    self.client_port = client_port

  def __send_socket(self, message: bytes, ip_address=None, port=None):
    try:
      port = port or self.devices_port

      if ip_address is None:
        return

      client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      client_socket.connect((ip_address, port))

      client_socket.sendall(message)
      client_socket.close()
    except Exception as e:
      print(e)
      print("Falha ao mandar socket")

  def __discover_devices(self):
    sock = socket.socket(
      socket.AF_INET,  # familia de ips ipv4
      socket.SOCK_DGRAM,  # socket baseado em datagramas (UDP)
      socket.IPPROTO_UDP,  # protocolo UDP
    )

    sock.setsockopt(
      socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2
    )  # Definir o TTL do multicast no nivel IP
    sock.setsockopt(
      socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton("MCAST_IF_IP")
    )

    try:
      while True:
        message = message_pb2.Message()
        message.type = message_pb2.DEVICE_DISCOVERY
        serialized_message = message.SerializeToString()

        print(
          f"Enviando: mensagem de descoberta para {self.multicast_group_ip}:{self.multicast_group_port}"
        )
        sock.sendto(
          serialized_message,
          (self.multicast_group_ip, self.multicast_group_port),
        )
        time.sleep(self.discover_interval_in_seconds)
    except Exception as e:
      print(f"Erro na thread de envio: {e}")
    finally:
      sock.close()

  def __get_device(self, device_id) -> dict | None:
    for device in self.registered_devices:
      if device["id"] == device_id:
        return device

  def __listen_messages(self):
    server_socket = socket.socket(
      socket.AF_INET,  # familia de ips ipv4
      socket.SOCK_STREAM,  # socket orientado a conexão (TCP)
    )
    server_socket.bind((self.tcp_listen_ip, self.tcp_listen_port))
    server_socket.listen(10)

    try:
      while True:
        client_socket, client_address = server_socket.accept()

        data = client_socket.recv(1024)
        if data:
          message = message_pb2.ForwardedMessage()
          message.ParseFromString(data)
          if message.content.type == message_pb2.REGISTER_DEVICE:
            print(f"Dispositivo pedindo para se registrar: {client_address}")
            self.device_counter += 1
            new_device = {
              "id": self.device_counter,
              "ip_address": client_address[0],
              "type": message.content.params[0],
            }
            self.registered_devices.append(new_device)

            message = message_pb2.Message()
            message.type = message_pb2.REGISTER_DEVICE
            message.params.append(new_device["id"])
            message.params.append(new_device["type"])
            serialized_message = message.SerializeToString()
            self.__send_socket(serialized_message, self.client_ip, self.client_port)

          elif message.content.type == message_pb2.TEMPERATURE_INFO:
            print(
              f"Temperatura do ar condicionado recebida! {message.content.params[0]} graus!"
            )
            serialized_message = message.content.SerializeToString()
            self.__send_socket(serialized_message, self.client_ip, self.client_port)
          else:
            print(
              f"Mensagem recebida do tipo {message_types[message.content.type]} enviada para o dispositivo de id {message.id}"
            )
            device = self.__get_device(message.id)
            if device:
              serialized_message = message.content.SerializeToString()
              self.__send_socket(
                serialized_message, device["ip_address"], self.devices_port
              )

        client_socket.close()
    finally:
      server_socket.close()

  def start(self):
    # Iniciar threads para envio e recepção
    sender_thread = Thread(target=self.__discover_devices, daemon=True)
    receiver_thread = Thread(target=self.__listen_messages, daemon=True)

    sender_thread.start()
    receiver_thread.start()

    try:
      while True:
        time.sleep(1)
    except KeyboardInterrupt:
      print("\nEncerrando o gateway.")
