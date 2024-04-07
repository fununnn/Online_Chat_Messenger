import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = '127.0.0.1'
server_port = 9001

host = socket.gethostname()
address = socket.gethostbyname(host)
port = 9050
message = b'Message to send to the client.'+ input("input your messege").encode('utf-8')

# 空の文字列も0.0.0.0として使用できます。
sock.bind((address,port))

try:
  print('sending {!r}'.format(message))
  # サーバへのデータ送信
  sent = sock.sendto(message, (server_address, server_port))
  print('Send {} bytes'.format(sent))

  # 応答を受信
  print('waiting to receive')
  data, server = sock.recvfrom(4096)
  print('received {!r}'.format(data))

finally:
  print('closing socket')
  sock.close()