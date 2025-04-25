# === GENERATORE DI LIVELLI ===
import random
from collections import deque

import config
from directions import DIRS


# === PATHFINDING ===
def bfs(start, goal, game_map, avoid=None):
    if avoid is None:
        avoid = []
    queue = deque()
    queue.append((start, []))
    visited = {start}
    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == goal:
            return path
        for dx, dy in DIRS.values():
            nx, ny = x + dx, y + dy
            if (0 <= nx < config.MAP_WIDTH and 0 <= ny < config.MAP_HEIGHT and
                game_map[ny][nx] == 1 and (nx, ny) not in visited and (nx, ny) not in avoid):
                queue.append(((nx, ny), path + [(nx, ny)]))
                visited.add((nx, ny))
    return []


def generate_random_level(width=10, height=10, walk_length=50, num_enemies=3, seed=None):
    if seed is not None:
        random.seed(seed)
    dungeon = [[0 for _ in range(width)] for _ in range(height)]
    x, y = width // 2, height // 2
    dungeon[y][x] = 1
    visited = [(x, y)]
    for _ in range(walk_length):
        dx, dy = random.choice([(0,1), (0,-1), (1,0), (-1,0)])
        nx, ny = x + dx, y + dy
        if 1 <= nx < width-1 and 1 <= ny < height-1:
            x, y = nx, ny
            dungeon[ny][nx] = 1
            visited.append((nx, ny))
    player_start = visited[0]
    far_tiles = [pos for pos in visited if abs(pos[0] - player_start[0]) + abs(pos[1] - player_start[1]) > 5]
    key_pos = random.choice(far_tiles) if far_tiles else random.choice(visited)
    enemy_positions = random.sample([p for p in visited if p != player_start and p != key_pos], min(num_enemies, len(visited)-2))
    return {
        "map": dungeon,
        "player_start": player_start,
        "key": key_pos,
        "enemies": enemy_positions
    }


# === LOAD LEVEL ===
def load_level(level_data):
    config.game_map = level_data["map"]
    config.player_x, config.player_y = level_data["player_start"]
    config.enemies = level_data["enemies"]
    config.key_pos = level_data.get("key")
    config.exit_pos = None
    config.has_key = False
    config.level_complete = False
    config.game_over = False


# === AVANZA LIVELLO ===
def next_level():
    config.current_level += 1
    config.player_score += 500
    config.player_lives = min(5, config.player_lives + 1)
    level_data = generate_random_level(width=config.MAP_WIDTH, height=config.MAP_HEIGHT, seed=config.current_level)
    load_level(level_data)
