from game import Game
import pygame
import sys
import random

WHITE = (255, 255, 255)
GREY = (70, 70, 70)
BLACK = (0, 0, 0)
FOOD_COLOR = (200, 0, 0)
SNAKE_COLORS = [(0, 255, 0), (53, 98, 191), (155, 180, 0), (155, 98, 0), (116, 98, 191), (18, 188, 210), (0, 100, 0)]

LEFT  = 0
UP    = 1
RIGHT = 2
DOWN  = 3

WINDOW_HEIGHT = 750
WINDOW_WIDTH = 750
BLOCK_SIZE = 15
GRID_HEIGHT = WINDOW_HEIGHT // BLOCK_SIZE
GRID_WIDTH = WINDOW_WIDTH // BLOCK_SIZE
GAME = Game()

pygame.init()
SCREEN = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))

def main():
    random.seed(1)

    global SCREEN, CLOCK, NAME, GAME
    GAME.spawn_snake(1, "snake", [(10, 10), (11, 10), (12, 10)])
    sleep_clock = pygame.time.Clock()
    CLOCK = pygame.time.Clock()

    direction = RIGHT

    iteration = 0

    while True:
        if iteration % 50 == 0:
            x, y = random.randint(0, 50) - 1, random.randint(0, 50) - 1
            GAME.spawn_food((x, y))
        iteration += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != UP:
                    direction = DOWN
        
        GAME.apply_snake_movements([(1, direction)])

        pygame.display.update()
        drawGrid()
        sleep_clock.tick(15)


def drawGrid():
    global GAME, BLOCK_SIZE, SCREEN, GRID_HEIGHT, GRID_WIDTH
    grid = GAME.map_repr()
    SCREEN.fill(BLACK)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(y*BLOCK_SIZE, x*BLOCK_SIZE,
                               BLOCK_SIZE, BLOCK_SIZE)
            border = False
            CELL_COLOR = GREY
            if grid[y][x] == 1:
                CELL_COLOR = FOOD_COLOR
            elif grid[y][x] >= 10:
                CELL_COLOR = SNAKE_COLORS[grid[y][x] % 10]
                if grid[y][x] // 10 == 1:
                    r, g, b = CELL_COLOR
                    CELL_COLOR = (255, g, b)
            else:
                border = True
            pygame.draw.rect(SCREEN, CELL_COLOR, rect, border)

if __name__ == "__main__":
    main()
