import socket

# UDPクライアントの設定
UDP_IP = '127.0.0.1'
UDP_PORT = 9002

# チャットルーム情報
room_name = 'room1'
token = b'participant1_token'

# UDPソケットの作成
udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    message = input('Enter message: ')

    # メッセージを送信
    room_name_bytes = room_name.encode('utf-8')
    room_name_size = len(room_name_bytes)
    token_size = len(token)
    data = bytearray(2 + room_name_size + token_size + len(message))
    data[0] = room_name_size
    data[1] = token_size
    data[2:2+room_name_size] = room_name_bytes
    data[2+room_name_size:2+room_name_size+token_size] = token
    data[2+room_name_size+token_size:] = message.encode('utf-8')

    udp_client_socket.sendto(data, (UDP_IP, UDP_PORT))

    # 受信ループ
    while True:
        try:
            response, addr = udp_client_socket.recvfrom(4096)
            print(f'Received message: {response.decode("utf-8")}')
        except BlockingIOError:
            break