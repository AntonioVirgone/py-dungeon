# === CONFIG ===
TILE_SIZE = 40
MAP_WIDTH, MAP_HEIGHT = 10, 10
SCREEN_WIDTH = TILE_SIZE * MAP_WIDTH
SCREEN_HEIGHT = TILE_SIZE * MAP_HEIGHT
ENEMY_MOVE_DELAY = 30


# === GLOBAL GAME STATE ===
player_x = player_y = 1
player_dir = "RIGHT"
player_lives = 3
player_score = 0
enemies = []
game_map = []
key_pos = None
exit_pos = None
has_key = False
level_complete = False
game_over = False
current_level = 0