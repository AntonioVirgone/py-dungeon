import random
from collections import deque
import pygame
import sys
import os

from constant import *
from enemy import enemy_generator
from map_generator import genera_mappa, is_cell_empty

# Inizializza pygame
pygame.init()

game_map = genera_mappa(MAP_WIDTH)


# Posizione iniziale del player
player_x, player_y = game_map[1][1], game_map[1][1]
player_dir = "RIGHT"
player_lives = 3
player_score = 0


# Posizione iniziale dei nemici
enemies = enemy_generator()
key_pos = None
exit_pos = None
has_key = False

# Funzione per caricare e scalare immagini
def load_image(name):
    return pygame.transform.scale(pygame.image.load(os.path.join(name)), (TILE_SIZE, TILE_SIZE))


# Funzione di pathfinding (BFS)
def bfs(start, goal, game_map, avoid=[]):
    queue = deque()
    queue.append((start, []))
    visited = {start}

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

# Crea la finestra
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler - Nemici e Armi")


# Carica le immagini
floor_img = load_image("floor.png")
wall_img = load_image("wall.png")
player_img = load_image("player.png")
enemy_img = load_image("enemy.png")
key_img = load_image("key.png")
exit_img = load_image("exit.png")


# Scala le immagini alla dimensione del tile
floor_img = pygame.transform.scale(floor_img, (TILE_SIZE, TILE_SIZE))
wall_img = pygame.transform.scale(wall_img, (TILE_SIZE, TILE_SIZE))
player_img = pygame.transform.scale(player_img, (TILE_SIZE, TILE_SIZE))
enemy_img = pygame.transform.scale(enemy_img, (TILE_SIZE, TILE_SIZE))


# Clock per il framerate
clock = pygame.time.Clock()
frame_count = 0
game_over = False
level_complete = False


# Game loop
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

            new_x, new_y = player_x + dx, player_y + dy
            if game_map[new_y][new_x] == 1:
                player_x, player_y = new_x, new_y

            # Raccoglie la chiave
            if key_pos and (player_x, player_y) == key_pos:
                has_key = True
                key_pos = None
                exit_pos = (8, 8)  # abilita l'uscita

            # Passaggio livello
            if has_key and exit_pos and (player_x, player_y) == exit_pos:
                level_complete = True

            # Attacco
            if event.key == pygame.K_SPACE:
                atk_dx, atk_dy = DIRS[player_dir]
                atk_x, atk_y = player_x + atk_dx, player_y + atk_dy
                if (atk_x, atk_y) in enemies:
                    enemies.remove((atk_x, atk_y))
                    player_score += 100
                    # Possibile drop chiave
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
                new_enemies.append((ex, ey))  # resta fermo se bloccato
        enemies = new_enemies

    # Disegno del livello
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            img = floor_img if game_map[y][x] == 1 else wall_img
            screen.blit(img, (x * TILE_SIZE, y * TILE_SIZE))

    # Oggetti
    if key_pos:
        screen.blit(key_img, (key_pos[0] * TILE_SIZE, key_pos[1] * TILE_SIZE))
    if exit_pos and has_key:
        screen.blit(exit_img, (exit_pos[0] * TILE_SIZE, exit_pos[1] * TILE_SIZE))

    # Player
    screen.blit(player_img, (player_x * TILE_SIZE, player_y * TILE_SIZE))

    # Nemici
    for ex, ey in enemies:
        screen.blit(enemy_img, (ex * TILE_SIZE, ey * TILE_SIZE))

    # HUD
    font = pygame.font.SysFont(None, 24)
    hud = font.render(f"Vite: {player_lives}  Punti: {player_score}", True, (255, 255, 255))
    screen.blit(hud, (10, 10))

    # Game Over / Next Level
    if game_over:
        text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))
    elif level_complete:
        text = font.render("LIVELLO COMPLETATO!", True, (0, 255, 0))
        screen.blit(text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2))

    pygame.display.flip()
    clock.tick(60)
    frame_count += 1


# Chiude pygame
pygame.quit()
sys.exit()

