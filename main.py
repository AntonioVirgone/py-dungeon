from collections import deque
import pygame
import sys
import os
import random


# Inizializza pygame
pygame.init()


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


# Mappa (0 = muro, 1 = pavimento)
game_map = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,0,1,1,1,1,0],
    [0,1,0,1,0,1,0,0,1,0],
    [0,1,0,1,1,1,0,1,1,0],
    [0,1,0,0,0,1,0,1,0,0],
    [0,1,1,1,0,1,1,1,0,0],
    [0,0,0,1,0,0,0,1,1,0],
    [0,1,1,1,1,1,0,0,1,0],
    [0,1,0,0,0,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0],
]


# Posizione iniziale del player
player_x, player_y = 1, 1

# Posizione iniziale dei nemici
enemies = [(7, 1), (5, 5)]  # due nemici


# Crea la finestra
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler - Nemici e Armi")


# Carica le immagini
floor_img = pygame.image.load("floor.png")
wall_img = pygame.image.load("wall.png")
player_img = pygame.image.load("player.png")
enemy_img = pygame.image.load("enemy.png")


# Scala le immagini alla dimensione del tile
floor_img = pygame.transform.scale(floor_img, (TILE_SIZE, TILE_SIZE))
wall_img = pygame.transform.scale(wall_img, (TILE_SIZE, TILE_SIZE))
player_img = pygame.transform.scale(player_img, (TILE_SIZE, TILE_SIZE))
enemy_img = pygame.transform.scale(enemy_img, (TILE_SIZE, TILE_SIZE))


# Clock per il framerate
clock = pygame.time.Clock()
frame_count = 0

# Game loop
running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not game_over:
            new_x, new_y = player_x, player_y
            if event.key == pygame.K_LEFT:
                new_x -= 1
            elif event.key == pygame.K_RIGHT:
                new_x += 1
            elif event.key == pygame.K_UP:
                new_y -= 1
            elif event.key == pygame.K_DOWN:
                new_y += 1

            # Controllo se la nuova posizione è valida (pavimento)
            if game_map[new_y][new_x] == 1:
                player_x, player_y = new_x, new_y

    if not game_over:
        # Movimento nemici ogni ENEMY_MOVE_DELAY frame
        if frame_count % ENEMY_MOVE_DELAY == 0:
            new_enemies = []
            for (ex, ey) in enemies:
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                random.shuffle(directions)
                moved = False
                for dx, dy in directions:
                    nx, ny = ex + dx, ey + dy
                    if (0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT and
                            game_map[ny][nx] == 1 and (nx, ny) != (player_x, player_y)):
                        new_enemies.append((nx, ny))
                        moved = True
                        break
                if not moved:
                    new_enemies.append((ex, ey))  # resta fermo
            enemies = new_enemies

        # Controllo collisioni con player
        if (player_x, player_y) in enemies:
            game_over = True

    # Disegna la mappa
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            img = floor_img if game_map[y][x] == 1 else wall_img
            screen.blit(img, (x * TILE_SIZE, y * TILE_SIZE))

    # Disegna il player
    screen.blit(player_img, (player_x * TILE_SIZE, player_y * TILE_SIZE))

    # Disegna i nemici
    for ex, ey in enemies:
        screen.blit(enemy_img, (ex * TILE_SIZE, ey * TILE_SIZE))

    # Messaggio di game over
    if game_over:
        font = pygame.font.SysFont(None, 48)
        text = font.render("GAME OVER", True, (255, 0, 0))
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, rect)

    # Aggiorna lo schermo
    pygame.display.flip()
    clock.tick(60)
    frame_count += 1


# Chiude pygame
pygame.quit()
sys.exit()

