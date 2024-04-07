import socket

# TCRPヘッダーの定義
HEADER_SIZE = 32
ROOM_NAME_SIZE_INDEX = 0
OPERATION_INDEX = 1
STATE_INDEX = 2
OPERATION_PAYLOAD_SIZE_INDEX = 3

# 操作コード
OPERATION_CREATE_ROOM = 1
OPERATION_JOIN_ROOM = 2

# 状態コード
STATE_REQUEST = 0
STATE_COMPLY = 1
STATE_COMPLETE = 2

# TCPサーバーの設定
TCP_IP = '127.0.0.1'
TCP_PORT = 9001

# チャットルームの管理
chat_rooms = {}

# TCPソケットの作成
tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server_socket.bind((TCP_IP, TCP_PORT))
tcp_server_socket.listen(5)

print(f'TCP Server listening on {TCP_IP}:{TCP_PORT}')

# 各操作を処理する関数
def handle_create_room(client_socket, state, room_name, operation_payload):
    if state == STATE_REQUEST:
        # リクエストを受け付ける
        response_payload = b'OK'
        send_response(client_socket, STATE_COMPLY, room_name, response_payload)

        # トークンを生成してクライアントに送信
        token = generate_token()
        chat_rooms[room_name] = {
            'host_token': token,
            'participants': []
        }
        send_response(client_socket, STATE_COMPLETE, room_name, token)

    else:
        # 無効な状態
        send_error(client_socket, room_name)

def handle_join_room(client_socket, state, room_name, operation_payload):
    if state == STATE_REQUEST:
        if room_name in chat_rooms:
            # リクエストを受け付ける
            response_payload = b'OK'
            send_response(client_socket, STATE_COMPLY, room_name, response_payload)

            # トークンを生成してクライアントに送信
            token = generate_token()
            chat_rooms[room_name]['participants'].append(token)
            send_response(client_socket, STATE_COMPLETE, room_name, token)
        else:
            # ルームが存在しない
            send_error(client_socket, room_name)
    else:
        # 無効な状態
        send_error(client_socket, room_name)

# 応答を送信する関数
def send_response(client_socket, state, room_name, payload):
    room_name_bytes = room_name.encode('utf-8')
    room_name_size = len(room_name_bytes)
    payload_size = len(payload)
    header = bytearray(HEADER_SIZE)
    header[ROOM_NAME_SIZE_INDEX] = room_name_size
    header[OPERATION_INDEX] = OPERATION_CREATE_ROOM
    header[STATE_INDEX] = state
    header[OPERATION_PAYLOAD_SIZE_INDEX:HEADER_SIZE] = payload_size.to_bytes(29, byteorder='big')
    client_socket.sendall(header + room_name_bytes + payload)

# エラー応答を送信する関数
def send_error(client_socket, room_name):
    error_payload = b'Error occurred'
    send_response(client_socket, STATE_COMPLY, room_name, error_payload)

# トークンを生成する関数
def generate_token():
    # ここではダミーのトークンを返すが、実際には適切なトークン生成ロジックが必要
    return b'dummy_token'

while True:
    client_socket, addr = tcp_server_socket.accept()
    print(f'Got connection from {addr}')

    # ヘッダーを受信
    header = client_socket.recv(HEADER_SIZE)
    if not header:
        continue

    # ヘッダー情報を解析
    room_name_size = header[ROOM_NAME_SIZE_INDEX]
    operation = header[OPERATION_INDEX]
    state = header[STATE_INDEX]
    operation_payload_size = int.from_bytes(header[OPERATION_PAYLOAD_SIZE_INDEX:HEADER_SIZE], byteorder='big')

    # ボディを受信
    body = client_socket.recv(room_name_size + operation_payload_size)
    room_name = body[:room_name_size].decode('utf-8')
    operation_payload = body[room_name_size:]

    # 操作に応じた処理
    if operation == OPERATION_CREATE_ROOM:
        handle_create_room(client_socket, state, room_name, operation_payload)
    elif operation == OPERATION_JOIN_ROOM:
        handle_join_room(client_socket, state, room_name, operation_payload)

    client_socket.close()