import socket
import common.constants as c
import common.settings as settings
import json
import threading
import select
from common.game import game
import sys

processed_UDP = {}  # id: 1

def send_join_request():
    msgPacket = {'ip': settings.MY_IP, 'type': c.JOIN_REQUEST, "name": settings.MY_NAME}
    if not __send_TCP(msgPacket):
        return False
    return True

def send_leave_request():
    msgPacket = {'id': game.get_my_snake_id(), 'type': c.LEAVE_REQUEST}
    __send_TCP(msgPacket)


def send_move_request(snake_id: int, direction: int):
    msgPacket = {'id': snake_id, 'type': c.MOVE_REQUEST, 'dir': direction}
    __send_TCP(msgPacket)

tcp_socket = None

def __link_TCP():
    global tcp_socket
    try:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.settimeout(3.0)
        tcp_socket.connect((settings.SERVER_IP, c.PORT))
    except Exception as e:
        print("✘ Could not establish link with server!")
        return False


def __send_TCP(msgPacket: dict):
    global tcp_socket
    if tcp_socket is None:
        __link_TCP()
    msgPacketBytes = json.dumps(msgPacket).encode(encoding='utf-8')
    try:
        tcp_socket.sendall(msgPacketBytes)
    except Exception:
        print("✘ Server is offline -> Couldn't send " + str(msgPacket) + ' to ' + settings.SERVER_IP)
        return False
    return True