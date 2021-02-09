# PyGame constants =========================
WHITE = (255, 255, 255)
GREY = (70, 70, 70)
BLACK = (0, 0, 0)
FOOD_COLOR = (200, 0, 0)
MY_SNAKE_COLOR = (0, 255, 0)
OTHER_SNAKES_COLOR = (53, 98, 191)

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
PORT = 12345
BUFFER_SIZE = 1500

# Client message types
JOIN_REQUEST = 0
LEAVE_REQUEST = 1
MOVE_REQUEST = 2

# Server UDP message types
SNAKES = 0
FOOD_SPAWN = 1
MOVEMENTS = 2
SNAKE_LEFT = 3
START_GAME = 4

# Game constants ===========================
MAP_SIZE = 50
PLAYER_LIMIT = 3
SERVER_TICK_SEC = 5
MAX_MOVEMENT_DIFF = 2.0 # Seconds