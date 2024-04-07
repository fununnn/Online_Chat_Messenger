import socket

# UDPサーバーの設定
UDP_IP = '0.0.0.0'
UDP_PORT = 9002

# チャットルームの管理
chat_rooms = {
    'room1': {
        'host_token': b'host_token_for_room1',
        'participants': [b'participant1_token', b'participant2_token']
    },
    'room2': {
        'host_token': b'host_token_for_room2',
        'participants': []
    }
}

# UDPソケットの作成
udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server_socket.bind((UDP_IP, UDP_PORT))

print(f'UDP Server listening on {UDP_IP}:{UDP_PORT}')

def handle_udp_message(data, addr):
    # ヘッダーを解析
    room_name_size = data[0]
    token_size = data[1]
    room_name = data[2:2+room_name_size].decode('utf-8')
    token = data[2+room_name_size:2+room_name_size+token_size].decode('utf-8')
    message = data[2+room_name_size+token_size:]

    # チャットルームが存在するかチェック
    if room_name in chat_rooms:
        room = chat_rooms[room_name]

        #トークンの有効性をチェック
        if token.encode('utf-8') == room['host_token'] or token in room['participants']:
            print(f'Received message from {addr} in room "{room_name}": {message.decode("utf-8")}')

            # メッセージをチャットルーム内の全参加者に転送
            for participant_token in room['participants']:
                if participant_token != token:
                    udp_server_socket.sendto(message, get_participant_address(participant_token))

        else:
            print(f'Invalid token for room "{room_name}":{token}')
    else:
        print(f'Room "{room_name}" does not exist')

# 参加者のIPアドレスを取得する関数（ダミー実装）
def get_participant_address(token):
    return ('127.0.0.1', 9003)

while True:
    data, addr = udp_server_socket.recvfrom(4096)
    handle_udp_message(data, addr)

