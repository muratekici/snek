import socket
from common import constants as c
import json
import threading
import select
from main import game

processed_UDP = {}  # id: 1


def start_listening():
    threading.Thread(target=__listen_UDP, daemon=True).start()


def send_join_request():
    msgPacket = {'my_ip': c.MY_IP, 'type': c.JOIN_REQUEST}
    _send_TCP(msgPacket=msgPacket)


def send_move_request():
    msgPacket = {'snake_id': c.MY_SNAKE_ID,
                 'type': c.MOVEMENT_REQUEST, 'direction': 0}
    _send_TCP(msgPacket=msgPacket)


def _send_TCP(msgPacket: dict):
    msgPacketBytes = json.dumps(msgPacket).encode(encoding='utf-8')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(3.0)
        try:
            s.connect((c.SERVER_IP, c.PORT))
            s.sendall(msgPacketBytes)
        except:
            print("✘ Unexpected offline client detected -> Couldn't send " +
                  type + ' to ' + c.SERVER_IP)
        else:
            print('✔ ' + type + ' to: ' + c.SERVER_IP)

# FOR SERVER

# def __send_UDP(msgPacket: dict):
#     msgPacketBytes = json.dumps(msgPacket).encode(encoding='utf-8')

#     for _ in range(3):
#         with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
#             s.bind(('', 0))
#             s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
#             s.sendto(msgPacketBytes, ('<broadcast>', c.PORT))


# def __listen_TCP():
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.bind((c.MY_IP, c.PORT))
#         s.listen()

#         while 1:
#             conn, addr = s.accept()
#             with conn:
#                 data = conn.recv(c.BUFFER_SIZE)

#                 if not data:
#                     continue

#                 threading.Thread(target=__handle_received_TCP,
#                                  args=[data], daemon=True).start()


def __listen_UDP():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(('', c.PORT))
        s.setblocking(0)

        while 1:
            result = select.select([s], [], [])
            data = result[0][0].recv(c.BUFFER_SIZE)

            threading.Thread(target=__handle_received_UDP,
                             args=[data], daemon=True).start()


def __handle_received_UDP(data: bytes):
    try:
        msgPacket = json.loads(data.decode('utf-8'))

        if msgPacket['id'] in processed_UDP:
            return
        processed_UDP[msgPacket['id']] = 1
        
        if msgPacket['type'] == c.SNAKE_SPAWN:
            if msgPacket['snake_ip'] == c.MY_IP:
                c.MY_SNAKE_ID = msgPacket['snake_id']
                
            placement = map(lambda coord: (coord[0], coord[1]), msgPacket['placement'])
            game.spawn_snake(snake_id=msgPacket['snake_id'], name=msgPacket['snake_name'], placement=placement)
        # TODO: handle message packet
    except:
        print('⚠ Message format wrong')


# def __handle_received_TCP(data: bytes):
#     try:
#         msgPacket = json.loads(data.decode('utf-8'))
#         # TODO: handle message packet
#     except:
#         print('⚠ Message format wrong')
