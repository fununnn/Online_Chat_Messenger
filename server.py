import socket
import os
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = '0.0.0.0'
server_port = 9001

print('starting up on port {}'.format(server_port))

dpath = 'temp'
if not os.path.exists(dpath):
    os.mkdir(dpath)

sock.bind((server_address, server_port))
connected_clients = {}
client_last_messege_time = {}
CLIENT_TIMEOUT = 10

def updateClientLastMessegeTime(client_address):
    client_last_messege_time[client_address] = time.time()

#接続の確立
while True:
    print('\nwaiting to receive message')
    byteData, address = sock.recvfrom(4096)
    print('received {} bytes from {}'.format(len(byteData), address))
    
    #クライアントの受信時刻更新
    updateClientLastMessegeTime(address)
    print(client_last_messege_time.get(address,"no messege recieved yet"))

    #各ヘッダ情報を格納
    header = byteData[:8]
    filename_length = int.from_bytes(header[:1],"big")
    json_length = int.from_bytes(header[1:4],"big")
    data_length = int.from_bytes(header[4:],"big")
    
    print('Received byteData from client. Byte lengths: Title length {}, JSON length {}, Data Length {}'.format(filename_length, json_length,data_length))
    
    #ファイル名の読み取り
    filename = byteData[8:8+filename_length].decode('utf-8')
    print(f"Filename:{filename}")
    
    #データが来た時のみ処理を行う
    if data_length > 0:
        file_path = os.path.join(dpath, filename)
        with open(file_path,'wb+') as f:
            f.write(byteData[8:8+filename_length:])
            print('Finished downloading the file from client.')

    #クライアントを辞書に追加
    sender_id = address[1]
    if sender_id not in connected_clients:
        connected_clients[sender_id]= address

    sent = sock.sendto(byteData, address)
    print(f'sent {sent} bytes back to {address}')