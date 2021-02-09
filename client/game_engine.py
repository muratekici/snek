import pygame
import time
from common import constants as c
from client.sender import send_move_request, send_leave_request

direction = c.RIGHT
last_direction = c.RIGHT
game_obj = None
pygame.init()
screen = pygame.display.set_mode((c.WINDOW_HEIGHT, c.WINDOW_WIDTH))


def init_game_engine(game: any):
    global direction, game_obj
    game_obj = game

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                send_leave_request()
                return
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and last_direction != c.RIGHT:
                    direction = c.LEFT
                elif (event.key == pygame.K_UP or event.key == pygame.K_w) and last_direction != c.DOWN:
                    direction = c.UP
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and last_direction != c.LEFT:
                    direction = c.RIGHT
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and last_direction != c.UP:
                    direction = c.DOWN
        # BLOCK_REFRESH = True
        # while BLOCK_REFRESH == True:
        #     pass


def __drawGrid(game: any, screen):
    grid = game.map_repr()
    screen.fill(c.BLACK)

    for i in range(c.GRID_HEIGHT):
        for j in range(c.GRID_WIDTH):
            i_pos = i*c.BLOCK_SIZE
            j_pos = j*c.BLOCK_SIZE
            rect = pygame.Rect(j_pos, i_pos,
                               c.BLOCK_SIZE, c.BLOCK_SIZE)
            border = False
            cell_color = c.GREY
            if grid[i][j] == 1:
                cell_color = c.FOOD_COLOR
            elif grid[i][j] >= 10:
                if grid[i][j] % 10 == 0:
                    cell_color = c.MY_SNAKE_COLOR
                else:
                    cell_color = c.OTHER_SNAKES_COLOR
                # If head
                if grid[i][j] // 10 == 1:
                    r, g, b = cell_color
                    cell_color = (255, g, b)
            else:
                border = True
            pygame.draw.rect(screen, cell_color, rect, border)


def progress_game():
    global direction, last_direction
    pygame.display.update()
    __drawGrid(game=game_obj, screen=screen)
    time.sleep(0.05)
    if game_obj.get_my_snake_id():
        last_direction = direction
        send_move_request(game_obj.get_my_snake_id(), direction)
