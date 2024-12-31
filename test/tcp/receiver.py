import socket

TCP_LISTEN_IP = "0.0.0.0"
TCP_LISTEN_PORT = 5001

server_socket = socket.socket(
  socket.AF_INET,  # familia de ips ipv4
  socket.SOCK_STREAM,  # socket orientado a conexão (TCP)
)
server_socket.bind((TCP_LISTEN_IP, TCP_LISTEN_PORT))
server_socket.listen(10)

client_socket, client_address = server_socket.accept()
data = client_socket.recv(1024)
print(data.decode())
