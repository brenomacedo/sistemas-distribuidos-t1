import socket
import struct

MULTICAST_GROUP_IP = "224.0.0.1"
MULTICAST_GROUP_PORT = 5001

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("", MULTICAST_GROUP_PORT))

group = socket.inet_aton(MULTICAST_GROUP_IP)
mreq = struct.pack("4s4s", group, socket.inet_aton("10.0.0.106"))
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

data, address = sock.recvfrom(1024)
print(data.decode())
