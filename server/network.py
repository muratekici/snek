import socket
from common import constants as c
from common import settings
import json
import threading
from threading import Timer
import select
from common.game import game
import time
import sys

curr_snake_movements = {}
next_snake_id = 1
message_index = 1
time_step = 0
completed_steps = {}  # time_step:1

snakes_last_timestamp = {}
snake_timers = {}

started = False


def start_server():
    global started

    threading.Thread(target=__listen_TCP).start()
    print('Waiting for players to join...')
    input('Press enter to start the game!\n')
    print("Let's goooooo!!!!!")
    started = True
    msgPacket = {
        "type": c.START_GAME,
    }
    __send_UDP(msgPacket)

    i, j = game.get_coord_for_food()
    __send_food_spawn(i, j)


def __listen_TCP():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((settings.MY_IP, c.PORT))
        s.listen()
        while 1:
            conn, addr = s.accept()
            threading.Thread(target=listen_connection, args=[
                             conn], daemon=True).start()


def listen_connection(conn):
    with conn:
        while True:
            data = conn.recv(c.BUFFER_SIZE)
            if not data:
                continue
            __handle_received_TCP(data)


def __handle_received_TCP(data: bytes):
    try:
        msgPacket = json.loads(data.decode('utf-8'))
        if msgPacket['type'] == c.JOIN_REQUEST:
            __handle_join_request(msgPacket)
        elif msgPacket['type'] == c.LEAVE_REQUEST:
            __handle_leave_request(msgPacket)
        elif msgPacket['type'] == c.MOVE_REQUEST:
            __handle_move_request(msgPacket)
    except Exception as e:
        print(e)


def __send_UDP(msgPacket: dict):
    global message_index
    msgPacket['msg_ind'] = message_index
    message_index += 1
    # print('SENT:', msgPacket)
    msgPacketBytes = json.dumps(msgPacket).encode(encoding='utf-8')
    for _ in range(2):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind(('', 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            broadcast_str = '<broadcast>'
            if settings.MY_IP.startswith('25.'):
                broadcast_str = '25.255.255.255'
            s.sendto(msgPacketBytes, (broadcast_str, c.PORT))


def __send_food_spawn(i: int, j: int):
    msgPacket = {'type': c.FOOD_SPAWN, 'i': i, 'j': j}
    __send_UDP(msgPacket)


def __handle_join_request(msgPacket: dict):
    if game.snake_count() >= c.PLAYER_LIMIT or started:
        return

    print('JOINED:', msgPacket)

    global next_snake_id
    head_i, head_j, i, j = game.get_coord_for_snake()
    game.spawn_snake(snake_id=next_snake_id, snake_ip=msgPacket['ip'], name=msgPacket['name'], placement=[
                     (head_i, head_j), (i, j)])
    next_snake_id += 1
    msgPacket = {
        "type": c.SNAKES,
        "snakes": game.get_snakes_json(),
    }
    __send_UDP(msgPacket)


def __handle_leave_request(msgPacket: dict):
    __remove_snake(msgPacket['id'])


def __handle_move_request(msgPacket: dict):
    # Snake could be removed by snake_2_food
    if game.snake_exists(msgPacket['id']):
        if msgPacket['id'] in snake_timers:
            snake_timers[msgPacket['id']].cancel()
            snake_timers.pop(msgPacket['id'])

        curr_snake_movements[msgPacket['id']] = msgPacket['dir']
        __progress_if_available()


def __check_movement_diff(snake_id: int, curr_time: float):
    # No movement in-between
    if game.snake_exists(snake_id) and snakes_last_timestamp[snake_id] == curr_time:
        print('LATENCY KICK:', str(snake_id))
        __remove_snake(snake_id)


def __remove_snake(snake_id: int):
    print('REMOVING SNAKE:', str(snake_id))
    if game.snake_exists(snake_id):
        game.remove_snake(snake_id)
        if snake_id in curr_snake_movements:
            curr_snake_movements.pop(snake_id)
        if snake_id in snake_timers:
            snake_timers[snake_id].cancel()
            snake_timers.pop(snake_id)
        msgPacket = {
            "type": c.SNAKE_LEFT,
            "id": snake_id
        }
        __send_UDP(msgPacket)
        __progress_if_available()


def __progress_if_available():
    if len(curr_snake_movements) == game.snake_count():
        threading.Thread(target=__finalize_time_step, daemon=True).start()


def __finalize_time_step():
    global time_step

    for snake_id in curr_snake_movements.keys():
        curr_time = time.time()
        snakes_last_timestamp[snake_id] = curr_time
        t = Timer(c.MAX_MOVEMENT_DIFF, __check_movement_diff,
                args=[snake_id, curr_time])
        snake_timers[snake_id] = t
        t.start()

    completed_steps[time_step] = 1
    time_step += 1

    game.apply_snake_movements([(int(id), dir)
                                for id, dir in curr_snake_movements.items()])

    msgPacket = {'type': c.MOVEMENTS, 'movements': curr_snake_movements}
    __send_UDP(msgPacket)

    curr_snake_movements.clear()

    food_deficit = max(0, game.snake_count() - game.food_count())
    for _ in range(food_deficit):
        i, j = game.get_coord_for_food()
        game.spawn_food(coordinate=(i, j))
        __send_food_spawn(i, j)
