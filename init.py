import os
import sys

import pygame

import config
from Enemy import Enemy
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
    # Movimenti del player
    running = config.player.move(pygame=pygame) if config.player.move(pygame=pygame) is not None else True

    # Movimenti dei nemici
    enemy = Enemy(config=config)
    enemy.move(frame_count)

    for y in range(config.MAP_HEIGHT):
        for x in range(config.MAP_WIDTH):
            img = floor_img if config.game_map[y][x] == 1 else wall_img
            screen.blit(img, (x * config.TILE_SIZE, y * config.TILE_SIZE))

    if config.key_pos:
        screen.blit(key_img, (config.key_pos[0] * config.TILE_SIZE, config.key_pos[1] * config.TILE_SIZE))
    if config.exit_pos and config.has_key:
        screen.blit(exit_img, (config.exit_pos[0] * config.TILE_SIZE, config.exit_pos[1] * config.TILE_SIZE))

    screen.blit(player_img, (config.player.player_x * config.TILE_SIZE, config.player.player_y * config.TILE_SIZE))
    for ex, ey in config.enemies:
        screen.blit(enemy_img, (ex * config.TILE_SIZE, ey * config.TILE_SIZE))

    font = pygame.font.SysFont(None, 24)
    hud = font.render(f"Livello: {config.current_level}  Vite: {config.player.player_lives}  Punti: {config.player.player_score}", True, (255, 255, 255))
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
