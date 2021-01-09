import socket
import common.constants as c
import json
import threading
import select
from main import game
import sys

processed_UDP = {}  # id: 1

udp_listener_socket = None

def start_listening():
    threading.Thread(target=__listen_UDP, daemon=True).start()


def send_join_request():
    msgPacket = {'my_ip': c.MY_IP, 'type': c.JOIN_REQUEST, "name": c.MY_NAME}
    _send_TCP(msgPacket=msgPacket)


def send_leave_request():
    msgPacket = {'id': c.MY_SNAKE_ID, 'type': c.LEAVE_REQUEST}
    _send_TCP(msgPacket=msgPacket)

# TODO:
# def send_move_request():
#     msgPacket = {'snake_id': c.MY_SNAKE_ID,
#                  'type': c.MOVEMENT_REQUEST, 'direction': 0}
#     _send_TCP(msgPacket=msgPacket)


def _send_TCP(msgPacket: dict):
    msgPacketBytes = json.dumps(msgPacket).encode(encoding='utf-8')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(3.0)
        try:
            s.connect((c.SERVER_IP, c.PORT))
            s.sendall(msgPacketBytes)
        except:
            print("✘ Server is offline -> Couldn't send " +
                  type + ' to ' + c.SERVER_IP)
        else:
            print('✔ ' + type + ' to: ' + c.SERVER_IP)


def __listen_UDP():
    global udp_listener_socket

    udp_listener_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_listener_socket.bind(('', c.PORT))
    udp_listener_socket.setblocking(0)

    while 1:
        result = select.select([udp_listener_socket], [], [])
        data = result[0][0].recv(c.BUFFER_SIZE)

        threading.Thread(target=__handle_received_UDP,
                            args=[data], daemon=True).start()


def __handle_received_UDP(data: bytes):
    try:
        msgPacket = json.loads(data.decode('utf-8'))

        if len(processed_UDP.keys()) == 0:
            processed_UDP[msgPacket['msg_ind']] = 1
        elif msgPacket['msg_ind'] in processed_UDP:
            return
        elif msgPacket['msg_ind'] - 1 not in processed_UDP:
            udp_listener_socket.close()
            send_leave_request()
            sys.exit()

        processed_UDP[msgPacket['msg_ind']] = 1

        if msgPacket['type'] == c.SNAKES:
            __add_snakes(msgPacket=msgPacket)
        elif msgPacket['type'] == c.SNAKE_LEFT:
            __snake_left(msgpacke=msgPacket)
        # TODO: handle message packet
    except:
        print('⚠ Message format wrong')


def __add_snakes(msgPacket: dict):
    game.clear_snakes()

    for snake in msgPacket['snakes']:
        placement = [(snake['placement'][1], snake['placement'][0]),
                     (snake['placement'][3], snake['placement'][2])]
        game.spawn_snake(
            snake_id=snake['id'], name=snake['name'], placement=placement)

        if snake['ip'] == c.MY_IP:
            c.MY_SNAKE_ID = msgPacket['snake_id']


def __snake_left(msgPacket: dict):
    if msgPacket['id'] == c.MY_SNAKE_ID:
        udp_listener_socket.close()
        sys.exit()
    else:
        game.remove_snake(id=msgPacket['id'])
