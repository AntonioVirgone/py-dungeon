import random

from constant import MAP_WIDTH, MAP_HEIGHT
from map_generator import is_cell_empty

def enemy_generator():
    enemies = []  # due nemici

    for i in range(0, 2):
        while True:
            x_pos = random.randrange(MAP_WIDTH/2, MAP_WIDTH)
            y_pos = random.randrange(MAP_HEIGHT/2, MAP_HEIGHT)

            if is_cell_empty(x_pos, y_pos):
                enemies.append([x_pos, y_pos])
                break

    return enemies