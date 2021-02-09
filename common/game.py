from .snake import Snake
from . import util
from . import constants as c
import random
import time
import _thread
import sys

random.seed(time.time)


class Game(object):
    # snake_id: Snake object
    __snakes = {}

    # List of (i, j) coordinates
    __foods = []

    __my_snake_id = 0

    def print_snakes(self):
        for snake_id, snake in self.__snakes.items():
            print(snake)

    # Returns MAP_SIZE x MAP_SIZE 2D list.
    # 0:  Empty pixel
    # 1:  Food
    # 1N: Head of the Nth snake
    # 2N: Body of the Nth snake
    def map_repr(self) -> list:
        map_pixels = [[0 for _ in range(c.MAP_SIZE)]
                      for _ in range(c.MAP_SIZE)]

        for food_coord in self.__foods:
            map_pixels[food_coord[0]][food_coord[1]] = 1

        if self.__my_snake_id:
            snake = self.__snakes[self.__my_snake_id]
            head_coord = snake.placement[0]
            map_pixels[head_coord[0]][head_coord[1]] = 10

            for i in range(1, len(snake.placement)):
                body_coord = snake.placement[i]
                map_pixels[body_coord[0]][body_coord[1]] = 20

        for snake_id in self.__snakes:
            if snake_id == self.get_my_snake_id():
                continue

            snake = self.__snakes[snake_id]
            head_coord = snake.placement[0]
            map_pixels[head_coord[0]][head_coord[1]] = 11

            for i in range(1, len(snake.placement)):
                body_coord = snake.placement[i]
                map_pixels[body_coord[0]][body_coord[1]] = 21

        return map_pixels

    def set_my_snake_id(self, id: int) -> None:
        self.__my_snake_id = id

    def get_my_snake_id(self) -> int:
        return self.__my_snake_id

    def snake_count(self) -> int:
        return len(self.__snakes)

    def food_count(self) -> int:
        return len(self.__foods)

    def clear_snakes(self):
        self.__snakes.clear()

    def remove_snake(self, id: int):
        if id in self.__snakes:
            self.__snakes.pop(id)

    def snake_exists(self, snake_id:int) -> bool:
        return snake_id in self.__snakes

    def get_snakes_json(self) -> list:
        snakes = []

        for id, snake in self.__snakes.items():
            placement = []
            for coord in snake.placement:
                placement.append(coord[0])
                placement.append(coord[1])

            snakes.append({
                'ip': snake.snake_ip,
                'id': id,
                'name': snake.name,
                'placement': placement,
            })
        return snakes

    def spawn_snake(self, snake_id: int, snake_ip: str, name: str,  placement: list):
        snake = Snake(snake_id=snake_id, snake_ip=snake_ip,
                      name=name, placement=placement)
        self.__snakes[snake_id] = snake

    def spawn_food(self, coordinate: tuple):
        self.__foods.append(coordinate)

    def get_coord_for_food(self) -> tuple:
        map_repr = self.map_repr()
        while 1:
            i, j = random.randint(
                0, c.MAP_SIZE - 1), random.randint(0, c.MAP_SIZE - 1)
            if map_repr[i][j] == 0:
                return i, j

    def get_coord_for_snake(self) -> tuple:
        map_repr = self.map_repr()
        while 1:
            i, j = random.randint(c.MAP_SIZE // 4, c.MAP_SIZE - 1 - c.MAP_SIZE //
                                  4), random.randint(c.MAP_SIZE // 4, c.MAP_SIZE - 1 - c.MAP_SIZE // 4)
            direction = 2
            head_i, head_j = util.get_head_coord((i, j), direction)
            if map_repr[i][j] == 0 and map_repr[head_i][head_j] == 0:
                return head_i, head_j, i, j

    # snake_movements (list): list of (snake_id, direction) tuples
    def apply_snake_movements(self, snake_movements: list):
        dying_snake_ids = []

        for snake_id, direction in snake_movements:
            snake_dying = self.__handle_snake_update(
                snake=self.__snakes[snake_id], direction=direction)
            if snake_dying:
                dying_snake_ids.append(snake_id)

        for snake_id in dying_snake_ids:
            self.__snake_2_food(snake_id)

    def __handle_snake_update(self, snake: Snake, direction: int) -> bool:
        is_dying = self.__handle_crash(snake=snake, direction=direction)
        if not is_dying:
            snake.move(direction=direction)
            _ = self.__handle_eating(snake=snake)
        return is_dying

    def __handle_eating(self, snake: Snake) -> bool:
        for i in range(len(self.__foods)):
            if self.__foods[i][0] == snake.placement[0][0] and self.__foods[i][1] == snake.placement[0][1]:
                self.__foods.pop(i)
                snake.grow()
                return True
        return False

    def __handle_crash(self, snake: Snake, direction: int) -> bool:
        is_dying = False
        new_head_coord = util.get_head_coord(
            coord=snake.placement[0], direction=direction)

        if new_head_coord[0] >= c.MAP_SIZE or new_head_coord[1] >= c.MAP_SIZE or new_head_coord[0] < 0 or new_head_coord[1] < 0:
            return True

        # Crashing into a body
        snakes_with_body = self.__get_snakes_with_body(
            coordinate=new_head_coord)
        if len(snakes_with_body):
            return True

        # Crashing into a head
        snakes_with_head = self.__get_snakes_with_head(
            coordinate=new_head_coord)
        if len(snakes_with_head):
            for snake_id in snakes_with_head:
                target_snake = self.__snakes[snake_id]
                if snake.length <= target_snake.length:
                    return True

        return is_dying

    # Checks if a snake body is on the given coordinate. Returns its id
    def __get_snakes_with_body(self, coordinate: tuple) -> list:
        res = []
        for snake_id in self.__snakes:
            snake = self.__snakes[snake_id]

            for i in range(1, len(snake.placement)):
                snake_i = snake.placement[i][0]
                snake_j = snake.placement[i][1]
                if snake_i == coordinate[0] and snake_j == coordinate[1]:
                    res.append(snake.snake_id)

        return res

    # Checks if a snake head is on the given coordinate. Returns its id
    def __get_snakes_with_head(self, coordinate: tuple) -> list:
        res = []
        for snake_id in self.__snakes:
            snake = self.__snakes[snake_id]
            snake_i = snake.placement[0][0]
            snake_j = snake.placement[0][1]
            if snake_i == coordinate[0] and snake_j == coordinate[1]:
                res.append(snake.snake_id)

        return res

    def __snake_2_food(self, snake_id: int):
        snake = self.__snakes[snake_id]
        print("DEAD:", snake)

        if(snake and snake.snake_id in self.__snakes):
            for coordinate in snake.placement:
                self.__foods.append(coordinate)
            if snake.snake_id == self.__my_snake_id:
                self.__my_snake_id = None
            self.__snakes.pop(snake.snake_id)


game = Game()
