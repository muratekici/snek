from snake import Snake
import util

MAP_SIZE = 50
PLAYER_LIMIT = 3


class Game(object):
    # snake_id: Snake object
    __snakes = {}

    # List of (y, x) coordinates
    __foods = []

    def print_snakes(self):
        for snake_id, snake in self.__snakes.items():
            print(snake)

    # Returns MAP_SIZE x MAP_SIZE 2D list.
    # 0:  Empty pixel
    # 1:  Food
    # 1N: Head of the Nth snake
    # 2N: Body of the Nth snake
    def map_repr(self) -> list:
        map_pixels = [[0 for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]

        for food_coord in self.__foods:
            map_pixels[food_coord[0]][food_coord[1]] = 1

        snake_num = 0
        for snake_id in self.__snakes:
            snake = self.__snakes[snake_id]
            head_coord = snake.placement[0]
            map_pixels[head_coord[0]][head_coord[1]] = 10 + snake_num

            for i in range(1, len(snake.placement)):
                body_coord = snake.placement[i]
                map_pixels[body_coord[0]][body_coord[1]] = 20 + snake_num
            snake_num += 1

        return map_pixels

    def spawn_snake(self, snake_id: int, name: str,  placement: list):
        snake = Snake(snake_id=snake_id, name=name, placement=placement)
        self.__snakes[snake_id] = snake

    def spawn_food(self, coordinate: tuple):
        self.__foods.append(coordinate)

    # snake_movements (list): list of (snake_id, direction) tuples
    def apply_snake_movements(self, snake_movements: list):
        for snake_id, direction in snake_movements:
            self.__handle_snake_update(
                snake=self.__snakes[snake_id], direction=direction)

    def __handle_snake_update(self, snake: Snake, direction: int):
        is_crashing = self.__handle_crash(snake=snake, direction=direction)
        if not is_crashing:
            snake.move(direction=direction)
            is_eating = self.__handle_eating(snake=snake)

    def __handle_eating(self, snake: Snake) -> bool:
        for i in range(len(self.__foods)):
            if self.__foods[i][0] == snake.placement[0][0] and self.__foods[i][1] == snake.placement[0][1]:
                del self.__foods[i]
                snake.grow()
                return True
        return False

    def __handle_crash(self, snake: Snake, direction: int):
        new_head_coord = util.get_head_coord(
            coord=snake.placement[0], direction=direction)

        if new_head_coord[0] >= MAP_SIZE or new_head_coord[1] >= MAP_SIZE or new_head_coord[0] < 0 or new_head_coord[1] < 0:
            self.__snake_2_food(snake)

        body_snake = self.__have_snake_body(coordinate=new_head_coord)
        if body_snake != None and body_snake.snake_id != snake.snake_id:
            self.__snake_2_food(snake)

        head_snake = self.__have_snake_head(coordinate=new_head_coord)
        if head_snake != None and head_snake.snake_id != snake.snake_id:
            if snake.length >= head_snake.length:
                self.__snake_2_food(head_snake)
            elif snake.length <= head_snake.length:
                self.__snake_2_food(snake)

    # Checks if a snake body is on the given coordinate. Returns its id
    def __have_snake_body(self, coordinate: tuple) -> Snake:
        for snake_id in self.__snakes:
            snake = self.__snakes[snake_id]

            for i in range(1, len(snake.placement)):
                snake_y = snake.placement[i][0]
                snake_x = snake.placement[i][1]
                if snake_y == coordinate[0] and snake_x == coordinate[1]:
                    return snake

        return None

    # Checks if a snake head is on the given coordinate. Returns its id
    def __have_snake_head(self, coordinate: tuple) -> Snake:
        for snake_id in self.__snakes:
            snake = self.__snakes[snake_id]
            snake_y = snake.placement[0][0]
            snake_x = snake.placement[0][1]
            if snake_y == coordinate[0] and snake_x == coordinate[1]:
                return snake

        return None

    def __snake_2_food(self, snake: Snake):
        print(snake)
        for coordinate in snake.placement:
            self.__foods.append(coordinate)
        del self.__snakes[snake.snake_id]
