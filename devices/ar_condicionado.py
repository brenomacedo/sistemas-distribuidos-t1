import socket
import struct
import time
from threading import Thread


class ArCondicionado:
  gateway_ip: str | None = None

  def __init__(
    self,
    multicast_group_ip: str = "224.1.1.1",
    multicast_group_port: int = 5005,
    tcp_listen_ip: str = "0.0.0.0",
    tcp_listen_port: int = 5006,
  ):
    self.multicast_group_ip = multicast_group_ip
    self.multicast_group_port = multicast_group_port
    self.tcp_listen_ip = tcp_listen_ip
    self.tcp_listen_port = tcp_listen_port

  def __send_socket(
    self, message: str, ip_address: str | None = None, port: int | None = None
  ):
    ip_address: str = ip_address or self.gateway_ip
    port = port or self.tcp_listen_port

    if ip_address is None:
      return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip_address, port))

    client_socket.sendall(message.encode("utf-8"))
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
    print(f"Mensagem recebida do gateway {address}: {data.decode('utf-8')}")
    sock.close()

    # Substituir aqui a mensagem por uma codificacao de protobuff
    # das informacoes do device
    self.__send_socket("Mensagem de autenticacao do device")

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
          decoded_data = data.decode("utf-8")
          print(f"Dado recebido do gateway: {decoded_data}")
          # IF DATA.TIPO == MUDAR_TEMPERATURA, MUDAR A TEMPERATURA DO AR CONDICIONADO

        gateway_socket.close()
    finally:
      device_socket.close()

  def discover_and_listen(self):
    self.__discover_gateway()
    self.__listen_messages()

  def send_temperature(self):
    self.__send_socket("Temperatura nova do ar condicionado: 22 graus celsius")
    time.sleep(2)
    # try:
    # except Exception:
    #   print("Erro ao tentar enviar informacoes sobre a temperatura do ar condicionado.")

  def start(self):
    # Iniciar threads para envio e recepção
    listen_messages_thread = Thread(target=self.discover_and_listen, daemon=True)
    send_temperature_thread = Thread(target=self.send_temperature, daemon=True)

    listen_messages_thread.start()
    send_temperature_thread.start()

    try:
      while True:
        time.sleep(1)
    except KeyboardInterrupt:
      print("\nEncerrando o gateway.")


device = ArCondicionado()
device.start()
