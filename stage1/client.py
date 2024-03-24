import socket
import os
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = '127.0.0.1'
server_port = 9001

host = socket.gethostname()
address = socket.gethostbyname(host)
port = 9050
username = input("input your username.")
byte_username = username.encode('utf-8')

#header imformation
filename_length = len(byte_username)
header = filename_length.to_bytes(1,byteorder='big')
header += (0).to_bytes(3,byteorder='big')
header += len(byte_username).to_bytes(4,byteorder='big')

data = header + byte_username

sock.bind((address,port))

try:
  print(f'sending {data!r}')
  sent = sock.sendto(data, (server_address, server_port))
  print(f'Send {sent} bytes')

  print('waiting to receive')
  response, server = sock.recvfrom(4096)
  print(f'received {response!r}')

finally:
  print('closing socket')
  sock.close()