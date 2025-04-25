# === CONFIG ===
from Player import Player

TILE_SIZE = 40
MAP_WIDTH, MAP_HEIGHT = 20, 20
SCREEN_WIDTH = TILE_SIZE * MAP_WIDTH
SCREEN_HEIGHT = TILE_SIZE * MAP_HEIGHT
ENEMY_MOVE_DELAY = 30


# === GLOBAL GAME STATE ===
player = Player(1, 1, "RIGHT", 3, 0)
enemies = []
game_map = []
key_pos = None
exit_pos = None
has_key = False
level_complete = False
game_over = False
current_level = 0