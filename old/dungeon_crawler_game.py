import pygame
import sys
import os
import random
from collections import deque

# === CONFIG ===
TILE_SIZE = 40
MAP_WIDTH, MAP_HEIGHT = 10, 10
SCREEN_WIDTH = TILE_SIZE * MAP_WIDTH
SCREEN_HEIGHT = TILE_SIZE * MAP_HEIGHT
ENEMY_MOVE_DELAY = 30

# === DIRECTIONS ===
DIRS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
}

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

# === PYGAME INIT ===
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler - Livelli Infiniti")
clock = pygame.time.Clock()

def load_image(name):
    return pygame.transform.scale(pygame.image.load(os.path.join(name)), (TILE_SIZE, TILE_SIZE))

floor_img = load_image("resources/floor.png")
wall_img = load_image("resources/wall.png")
player_img = load_image("resources/player.png")
enemy_img = load_image("resources/enemy.png")
key_img = load_image("resources/key.png")
exit_img = load_image("resources/exit.png")

# === PATHFINDING ===
def bfs(start, goal, game_map, avoid=[]):
    queue = deque()
    queue.append((start, []))
    visited = set([start])
    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == goal:
            return path
        for dx, dy in DIRS.values():
            nx, ny = x + dx, y + dy
            if (0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT and
                game_map[ny][nx] == 1 and (nx, ny) not in visited and (nx, ny) not in avoid):
                queue.append(((nx, ny), path + [(nx, ny)]))
                visited.add((nx, ny))
    return []

# === GENERATORE DI LIVELLI ===
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
    global game_map, player_x, player_y, enemies
    global key_pos, exit_pos, has_key
    global level_complete, game_over
    game_map = level_data["map"]
    player_x, player_y = level_data["player_start"]
    enemies = level_data["enemies"]
    key_pos = level_data.get("key")
    exit_pos = None
    has_key = False
    level_complete = False
    game_over = False

# === AVANZA LIVELLO ===
def next_level():
    global current_level, player_score, player_lives
    current_level += 1
    player_score += 500
    player_lives = min(5, player_lives + 1)
    level_data = generate_random_level(seed=current_level)
    load_level(level_data)

# === PRIMO LIVELLO ===
next_level()
frame_count = 0

# === MAIN LOOP ===
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not game_over and not level_complete:
            dx, dy = 0, 0
            if event.key == pygame.K_LEFT:
                dx, dy = DIRS["LEFT"]
                player_dir = "LEFT"
            elif event.key == pygame.K_RIGHT:
                dx, dy = DIRS["RIGHT"]
                player_dir = "RIGHT"
            elif event.key == pygame.K_UP:
                dx, dy = DIRS["UP"]
                player_dir = "UP"
            elif event.key == pygame.K_DOWN:
                dx, dy = DIRS["DOWN"]
                player_dir = "DOWN"
            nx, ny = player_x + dx, player_y + dy
            if game_map[ny][nx] == 1:
                player_x, player_y = nx, ny
            if key_pos and (player_x, player_y) == key_pos:
                has_key = True
                key_pos = None
                exit_pos = random.choice([p for p in sum([[ (x, y) for x, val in enumerate(row) if val == 1 ] for y, row in enumerate(game_map)], []) if (x, y) != (player_x, player_y)])
            if has_key and exit_pos and (player_x, player_y) == exit_pos:
                level_complete = True
            if event.key == pygame.K_SPACE:
                atk_dx, atk_dy = DIRS[player_dir]
                atk_x, atk_y = player_x + atk_dx, player_y + atk_dy
                if (atk_x, atk_y) in enemies:
                    enemies.remove((atk_x, atk_y))
                    player_score += 100
                    if not has_key and not key_pos and random.random() < 0.5:
                        key_pos = (atk_x, atk_y)

    if not game_over and not level_complete and frame_count % ENEMY_MOVE_DELAY == 0:
        new_enemies = []
        for ex, ey in enemies:
            path = bfs((ex, ey), (player_x, player_y), game_map, enemies)
            if path:
                next_step = path[0]
                if next_step == (player_x, player_y):
                    player_lives -= 1
                    if player_lives <= 0:
                        game_over = True
                else:
                    new_enemies.append(next_step)
            else:
                new_enemies.append((ex, ey))
        enemies = new_enemies

    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            img = floor_img if game_map[y][x] == 1 else wall_img
            screen.blit(img, (x * TILE_SIZE, y * TILE_SIZE))

    if key_pos:
        screen.blit(key_img, (key_pos[0] * TILE_SIZE, key_pos[1] * TILE_SIZE))
    if exit_pos and has_key:
        screen.blit(exit_img, (exit_pos[0] * TILE_SIZE, exit_pos[1] * TILE_SIZE))

    screen.blit(player_img, (player_x * TILE_SIZE, player_y * TILE_SIZE))
    for ex, ey in enemies:
        screen.blit(enemy_img, (ex * TILE_SIZE, ey * TILE_SIZE))

    font = pygame.font.SysFont(None, 24)
    hud = font.render(f"Livello: {current_level}  Vite: {player_lives}  Punti: {player_score}", True, (255, 255, 255))
    screen.blit(hud, (10, 10))

    if game_over:
        text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(text, (SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2))
    elif level_complete:
        text = font.render("LIVELLO COMPLETATO!", True, (0, 255, 0))
        screen.blit(text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(1500)
        next_level()

    pygame.display.flip()
    clock.tick(60)
    frame_count += 1

pygame.quit()
sys.exit()
