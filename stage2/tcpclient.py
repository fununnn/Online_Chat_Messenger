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

# TCPクライアントの設定
TCP_IP = '127.0.0.1'
TCP_PORT = 9001

# TCPソケットの作成
tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client_socket.connect((TCP_IP, TCP_PORT))

# ユーザー入力
user_name = input('Enter your username: ')
room_name = input('Enter room name: ')
create_or_join = input('Create (c) or join (j) room? ')

if create_or_join.lower() == 'c':
    operation = OPERATION_CREATE_ROOM
else:
    operation = OPERATION_JOIN_ROOM

# ヘッダーを作成
room_name_bytes = room_name.encode('utf-8')
room_name_size = len(room_name_bytes)
operation_payload = user_name.encode('utf-8')
operation_payload_size = len(operation_payload)
header = bytearray(HEADER_SIZE)
header[ROOM_NAME_SIZE_INDEX] = room_name_size
header[OPERATION_INDEX] = operation
header[STATE_INDEX] = STATE_REQUEST
header[OPERATION_PAYLOAD_SIZE_INDEX:HEADER_SIZE] = operation_payload_size.to_bytes(29, byteorder='big')

# リクエストを送信
tcp_client_socket.sendall(header + room_name_bytes + operation_payload)

# 応答を受信
while True:
    header = tcp_client_socket.recv(HEADER_SIZE)
    if not header:
        break

    room_name_size = header[ROOM_NAME_SIZE_INDEX]
    operation = header[OPERATION_INDEX]
    state = header[STATE_INDEX]
    operation_payload_size = int.from_bytes(header[OPERATION_PAYLOAD_SIZE_INDEX:HEADER_SIZE], byteorder='big')

    room_name = tcp_client_socket.recv(room_name_size).decode('utf-8')
    operation_payload = tcp_client_socket.recv(operation_payload_size)

    if state == STATE_COMPLY:
        print(f'Server response: {operation_payload.decode("utf-8")}')
    elif state == STATE_COMPLETE:
        if operation == OPERATION_CREATE_ROOM:
            print(f'Room "{room_name}" created. Host token: {operation_payload}')
        elif operation == OPERATION_JOIN_ROOM:
            print(f'Joined room "{room_name}". Token: {operation_payload}')
        break

tcp_client_socket.close()