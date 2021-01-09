import socket
from common import constants as c
import json
import threading
import select
from main import game
import time

curr_snake_movements = {}

time_step = 0
completed_steps = {}  # time_step:1

def start_server():
    threading.Thread(target=__listen_TCP, daemon=True).start()
    threading.Thread(target=__start_ticking, daemon=True).start()

def __start_ticking():
    while 1:
        curr_time_step = time_step
        time.sleep(c.SERVER_TICK_SEC)
        if curr_time_step not in completed_steps:
            threading.Thread(target=__finalize_time_step, daemon=True).start()

def __send_UDP(msgPacket: dict):
    msgPacketBytes = json.dumps(msgPacket).encode(encoding='utf-8')

    for _ in range(3):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind(('', 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            s.sendto(msgPacketBytes, ('<broadcast>', c.PORT))


def __listen_TCP():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((c.MY_IP, c.PORT))
        s.listen()

        while 1:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(c.BUFFER_SIZE)

                if not data:
                    continue

                threading.Thread(target=__handle_received_TCP,
                                 args=[data], daemon=True).start()


def __handle_received_TCP(data: bytes):
    try:
        msgPacket = json.loads(data.decode('utf-8'))

        if msgPacket['type'] == c.JOIN_REQUEST:
            pass
        elif msgPacket['type'] == c.LEAVE_REQUEST:
            pass
        elif msgPacket['type'] == c.MOVE_REQUEST:
            __handle_move_request(msgPacket=msgPacket)
        # TODO: handle message packet
    except:
        print('⚠ Message format wrong')


def __handle_move_request(msgPacket: dict):
    curr_snake_movements[msgPacket['id']] = msgPacket['dir']
    if len(curr_snake_movements) == c.PLAYER_LIMIT:
        threading.Thread(target=__finalize_time_step, daemon=True).start()


def __finalize_time_step():
    global time_step

    completed_steps[time_step] = 1
    time_step += 1

    temp_curr_mov = curr_snake_movements.copy()
    curr_snake_movements.clear()

    movements = []
    for snake_id, direction in temp_curr_mov.items():
        movements.append(snake_id)
        movements.append(direction)

    msgPacket = {'type': c.MOVEMENTS, 'movements': movements}
    __send_UDP(msgPacket=msgPacket)

    game.apply_snake_movements(snake_movements=[(
        snake_id, direction) for snake_id, direction in temp_curr_mov.items()])
    food_deficit = max(0, game.snake_count() - game.food_count() - 1)
    for _ in range(food_deficit):
        game.spawn_food(coordinate=game.get_coord_for_food())
