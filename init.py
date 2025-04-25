import pygame
import sys
import os
import random

import config
from directions import DIRS
from level import next_level, bfs

# === PYGAME INIT ===
pygame.init()
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler - Livelli Infiniti")
clock = pygame.time.Clock()


def load_image(name):
    return pygame.transform.scale(pygame.image.load(os.path.join(name)), (config.TILE_SIZE, config.TILE_SIZE))


floor_img = load_image("resources/floor.png")
wall_img = load_image("resources/wall.png")
player_img = load_image("resources/player.png")
enemy_img = load_image("resources/enemy.png")
key_img = load_image("resources/key.png")
exit_img = load_image("resources/exit.png")


# === PRIMO LIVELLO ===
next_level()
frame_count = 0

# === MAIN LOOP ===
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not config.game_over and not config.level_complete:
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
            nx, ny = config.player_x + dx, config.player_y + dy
            if config.game_map[ny][nx] == 1:
                config.player_x, config.player_y = nx, ny
            if config.key_pos and (config.player_x, config.player_y) == config.key_pos:
                config.has_key = True
                config.key_pos = None
                config.exit_pos = random.choice([p for p in sum([[ (x, y) for x, val in enumerate(row) if val == 1 ] for y, row in enumerate(config.game_map)], []) if (x, y) != (config.player_x, config.player_y)])
            if config.has_key and config.exit_pos and (config.player_x, config.player_y) == config.exit_pos:
                config.level_complete = True
            if event.key == pygame.K_SPACE:
                atk_dx, atk_dy = DIRS[player_dir]
                atk_x, atk_y = config.player_x + atk_dx, config.player_y + atk_dy
                if (atk_x, atk_y) in config.enemies:
                    config.enemies.remove((atk_x, atk_y))
                    config.player_score += 100
                    if not config.has_key and not config.key_pos and random.random() < 0.5:
                        config.key_pos = (atk_x, atk_y)

    if not config.game_over and not config.level_complete and frame_count % config.ENEMY_MOVE_DELAY == 0:
        new_enemies = []
        for ex, ey in config.enemies:
            path = bfs((ex, ey), (config.player_x, config.player_y), config.game_map, config.enemies)
            if path:
                next_step = path[0]
                if next_step == (config.player_x, config.player_y):
                    config.player_lives -= 1
                    if config.player_lives <= 0:
                        config.game_over = True
                else:
                    new_enemies.append(next_step)
            else:
                new_enemies.append((ex, ey))
        config.enemies = new_enemies

    for y in range(config.MAP_HEIGHT):
        for x in range(config.MAP_WIDTH):
            img = floor_img if config.game_map[y][x] == 1 else wall_img
            screen.blit(img, (x * config.TILE_SIZE, y * config.TILE_SIZE))

    if config.key_pos:
        screen.blit(key_img, (config.key_pos[0] * config.TILE_SIZE, config.key_pos[1] * config.TILE_SIZE))
    if config.exit_pos and config.has_key:
        screen.blit(exit_img, (config.exit_pos[0] * config.TILE_SIZE, config.exit_pos[1] * config.TILE_SIZE))

    screen.blit(player_img, (config.player_x * config.TILE_SIZE, config.player_y * config.TILE_SIZE))
    for ex, ey in config.enemies:
        screen.blit(enemy_img, (ex * config.TILE_SIZE, ey * config.TILE_SIZE))

    font = pygame.font.SysFont(None, 24)
    hud = font.render(f"Livello: {config.current_level}  Vite: {config.player_lives}  Punti: {config.player_score}", True, (255, 255, 255))
    screen.blit(hud, (10, 10))

    if config.game_over:
        text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(text, (config.SCREEN_WIDTH // 2 - 60, config.SCREEN_HEIGHT // 2))
    elif config.level_complete:
        text = font.render("LIVELLO COMPLETATO!", True, (0, 255, 0))
        screen.blit(text, (config.SCREEN_WIDTH // 2 - 80, config.SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(1500)
        next_level()

    pygame.display.flip()
    clock.tick(60)
    frame_count += 1

pygame.quit()
sys.exit()
