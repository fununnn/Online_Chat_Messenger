import socket
import os

#ソケットの作成
sock = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)

server_address = 'socket_file.sock'

#初期化
try:
    os.unlink(server_address)
except FileExistsError:
    pass

print("Starting up on {}".format(server_address))

#bind
sock.bind(server_address)

#接続待ち
sock.listen(1)

#接続の確立
while True:
    connection , cliant_address = sock.accept()
    try:
        print('connection from',cliant_address)
        #データ読み込み
        data = connection.recv(4096)
        data_str = data.decode('utf-8')
        print('Recieved' + data_str)
        if data:
            response = 'Processing ' + data_str
            #データ送信
            connection.sendall(response.encode())
        else:
            print('no data from' + cliant_address)
            break
    #接続を閉じる
    finally:
        print('Closing current connection')
        connection.close()