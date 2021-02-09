import socket
import common.constants as c
import common.settings as settings
import json
import threading
import select
from common.game import game
import sys

from client.sender import send_join_request, send_leave_request
from client.game_engine import progress_game

processed_UDP = {}  # id: 1

def start_client():
    threading.Thread(target=__listen_UDP, daemon=True).start()
    if not send_join_request():
        return False
    return True

def __listen_UDP():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(('', c.PORT))
        s.setblocking(0)
        while 1:
            result = select.select([s], [], [])
            data = result[0][0].recv(c.BUFFER_SIZE)
            threading.Thread(target=__handle_received_UDP, args=[data], daemon=True).start()


def __handle_received_UDP(data: bytes):
    msgPacket = json.loads(data.decode('utf-8'))

    if len(processed_UDP.keys()) == 0:
        processed_UDP[msgPacket['msg_ind']] = 1
    elif msgPacket['msg_ind'] in processed_UDP:
        return
    elif msgPacket['msg_ind'] - 1 not in processed_UDP:
        send_leave_request()
        sys.exit()

    processed_UDP[msgPacket['msg_ind']] = 1

    if msgPacket['type'] == c.SNAKES:
        __add_snakes(msgPacket)
    elif msgPacket['type'] == c.SNAKE_LEFT:
        __snake_left(msgPacket)
    elif msgPacket['type'] == c.FOOD_SPAWN:
        __food_spawn(msgPacket)
    elif msgPacket['type'] == c.MOVEMENTS:
        __apply_movements(msgPacket)
    elif msgPacket['type'] == c.START_GAME:
        __start_game()


def __start_game():
    progress_game()


def __add_snakes(msgPacket: dict):
    game.clear_snakes()

    for snake in msgPacket['snakes']:
        placement = [(snake['placement'][0], snake['placement'][1]),
                     (snake['placement'][2], snake['placement'][3])]

        if snake['ip'] == settings.MY_IP:
            game.set_my_snake_id(snake['id'])

        game.spawn_snake(
            snake_id=snake['id'], snake_ip=snake['ip'], name=snake['name'], placement=placement)


def __snake_left(msgPacket: dict):
    if msgPacket['id'] == game.get_my_snake_id():
        game.set_my_snake_id(None)
    game.remove_snake(id=msgPacket['id'])


def __food_spawn(msgPacket: dict):
    i, j = msgPacket['i'], msgPacket['j']
    game.spawn_food((i, j))


def __apply_movements(msgPacket: dict):
    movements_unpacked = msgPacket['movements']
    movements = list(movements_unpacked.items())
    movements = [(int(id), dir) for id, dir in movements]
    game.apply_snake_movements(movements)
    progress_game()