import socket
import sys
from faker import Faker


fake = Faker()

#ソケットの作成
sock =socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
server_address = 'socket_file.sock'
print('connecting to {}'.format(server_address))

#接続
try:
    sock.connect(server_address)
except socket.error as err:
    print(err)
    sys.exit(1)

#送受信
try:
    meesage = b'Sending a message to the server side.\n' \
    + fake.name().encode('utf-8') \
    + fake.address().encode('utf-8') \
    + fake.text().encode('utf-8') 

    sock.sendall(meesage)
    #応答待ち時間設定
    sock.settimeout(2)

    try:
        while True:
            data = sock.recv(4096)
            data_str = data.decode('utf-8')
            if data:
                print('Server response: '+ data_str)
            else:
                break
    except TimeoutError:
        print("socket timeout,ending listening for sesrver message")
finally:
    print('close socket')
    sock.close()