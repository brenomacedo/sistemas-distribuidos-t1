import socket

MULTICAST_GROUP_IP = "224.0.0.1"
MULTICAST_GROUP_PORT = 5001

sock = socket.socket(
  socket.AF_INET,  # familia de ips ipv4
  socket.SOCK_DGRAM,  # socket baseado em datagramas (UDP)
  socket.IPPROTO_UDP,  # protocolo UDP
)

sock.setsockopt(
  socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2
)  # Definir o TTL do multicast no nivel IP
sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton("10.0.0.106"))


print(
  f"Enviando: mensagem de descoberta para {MULTICAST_GROUP_IP}:{MULTICAST_GROUP_PORT}"
)
sock.sendto(
  "hello world".encode(),
  (MULTICAST_GROUP_IP, MULTICAST_GROUP_PORT),
)
