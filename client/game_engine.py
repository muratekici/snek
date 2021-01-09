import pygame
import random
from common.game import Game
from common import constants as c


def init_game_engine(game: Game):
    random.seed(1)
    pygame.init()

    screen = pygame.display.set_mode((c.WINDOW_HEIGHT, c.WINDOW_WIDTH))

    game.spawn_snake(1, "snake", [(10, 10), (11, 10), (12, 10)])
    sleep_clock = pygame.time.Clock()

    direction = c.RIGHT
    iteration = 0

    while True:
        if iteration % 50 == 0:
            x, y = random.randint(0, 50) - 1, random.randint(0, 50) - 1
            game.spawn_food((x, y))
        iteration += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # TODO: terminate()
                pass
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != c.RIGHT:
                    direction = c.LEFT
                elif (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != c.DOWN:
                    direction = c.UP
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != c.LEFT:
                    direction = c.RIGHT
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != c.UP:
                    direction = c.DOWN

        game.apply_snake_movements([(1, direction)])

        pygame.display.update()
        __drawGrid(game=game, screen=screen)
        sleep_clock.tick(15)


def __drawGrid(game: Game, screen):
    grid = game.map_repr(my_id=c.MY_SNAKE_ID)
    screen.fill(c.BLACK)

    for y in range(c.GRID_HEIGHT):
        for x in range(c.GRID_WIDTH):
            x_pos = x*c.BLOCK_SIZE
            y_pos = y*c.BLOCK_SIZE
            rect = pygame.Rect(x_pos, y_pos,
                               c.BLOCK_SIZE, c.BLOCK_SIZE)
            border = False
            cell_color = c.GREY
            if grid[y][x] == 1:
                cell_color = c.FOOD_COLOR
            elif grid[y][x] >= 10:
                cell_color = c.SNAKE_COLORS[grid[y][x] % 10]
                if grid[y][x] // 10 == 1:
                    r, g, b = cell_color
                    cell_color = (255, g, b)
            else:
                border = True
            pygame.draw.rect(screen, cell_color, rect, border)
