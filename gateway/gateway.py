import socket
import time
from threading import Thread
from models import message_pb2


class Gateway:
  def __init__(
    self,
    multicast_group_ip: str = "224.1.1.1",
    multicast_group_port: int = 5005,
    tcp_listen_ip: str = "0.0.0.0",
    tcp_listen_port: int = 5008,
    discover_interval_in_seconds: int = 5,
  ):
    self.multicast_group_ip = multicast_group_ip
    self.multicast_group_port = multicast_group_port
    self.tcp_listen_ip = tcp_listen_ip
    self.tcp_listen_port = tcp_listen_port
    self.discover_interval_in_seconds = discover_interval_in_seconds

  # def __send_socket(self, message: str, ip_address: str, port: int | None = None):
  #   port = port or self.tcp_listen_port

  #   client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  #   client_socket.connect((ip_address, port))

  #   message = "Olá, servidor!".encode("utf-8")
  #   client_socket.sendall(message)
  #   client_socket.close()

  def __discover_devices(self):
    sock = socket.socket(
      socket.AF_INET,  # familia de ips ipv4
      socket.SOCK_DGRAM,  # socket baseado em datagramas (UDP)
      socket.IPPROTO_UDP,  # protocolo UDP
    )

    sock.setsockopt(
      socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2
    )  # Definir o TTL do multicast no nivel IP

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
        print(f"Conexão estabelecida com {client_address}")

        data = client_socket.recv(1024)
        if data:
          decoded_data = data.decode("utf-8")
          print(f"Dado recebido: {decoded_data}")
          # IF DATA.TIPO == AUTENTICACAO, REGISTRE O IP DO DEVICE E SUAS INFORMACOES

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
