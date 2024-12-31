import socket

TARGET_IP = "10.0.1.253"
PORT = 5001

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((TARGET_IP, PORT))

client_socket.sendall("hello world".encode())
client_socket.close()
