# Costanti
TILE_SIZE = 40
MAP_WIDTH = 10
MAP_HEIGHT = 10
SCREEN_WIDTH = TILE_SIZE * MAP_WIDTH
SCREEN_HEIGHT = TILE_SIZE * MAP_HEIGHT
ENEMY_MOVE_DELAY = 60 # numero di frame tra un movimento del nemico

# Direzioni
DIRS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
}
