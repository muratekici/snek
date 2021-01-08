# PyGame constants =========================
WHITE = (255, 255, 255)
GREY = (70, 70, 70)
BLACK = (0, 0, 0)
FOOD_COLOR = (200, 0, 0)
SNAKE_COLORS = [(0, 255, 0), (53, 98, 191), (155, 180, 0),
                (155, 98, 0), (116, 98, 191), (18, 188, 210), (0, 100, 0)]
# Directions
LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3

WINDOW_HEIGHT = 750
WINDOW_WIDTH = 750
BLOCK_SIZE = 15
GRID_HEIGHT = WINDOW_HEIGHT // BLOCK_SIZE
GRID_WIDTH = WINDOW_WIDTH // BLOCK_SIZE

# Communication constants ==================
MY_IP = ''
SERVER_IP = ''
PORT = 12345
BUFFER_SIZE = 1500

MY_SNAKE_ID = ''

# Client message types
JOIN_REQUEST = 0
MOVEMENT_REQUEST = 1

# Server UDP message types
SNAKE_SPAWN = 0
FOOD_SPAWN = 1
MOVEMENTS = 2