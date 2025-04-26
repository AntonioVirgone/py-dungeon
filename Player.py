import random

import config
from directions import DIRS


class Player:
    def __init__(self, player_x, player_y, player_dir, player_lives, player_score):
        self.player_x = player_x
        self.player_y = player_y
        self.player_dir = player_dir
        self.player_lives = player_lives
        self.player_score = player_score


    def move(self, pygame):
        global player_dir
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
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
                nx, ny = config.player.player_x + dx, config.player.player_y + dy
                if config.game_map[ny][nx] == 1:
                    config.player.player_x, config.player.player_y = nx, ny
                if config.key_pos and (config.player.player_x, config.player.player_y) == config.key_pos:
                    config.has_key = True
                    config.key_pos = None

                    valid_positions = [
                        (x, y)
                        for y, row in enumerate(config.game_map)
                        for x, val in enumerate(row)
                        if val == 1 and (x, y) != (config.player.player_x, config.player.player_y)
                    ]

                    config.exit_pos = random.choice(valid_positions)

                if config.has_key and config.exit_pos and (
                config.player.player_x, config.player.player_y) == config.exit_pos:
                    config.level_complete = True
                if event.key == pygame.K_SPACE:
                    atk_dx, atk_dy = DIRS[player_dir]
                    atk_x, atk_y = config.player.player_x + atk_dx, config.player.player_y + atk_dy
                    if (atk_x, atk_y) in config.enemies:
                        config.enemies.remove((atk_x, atk_y))
                        config.player.player_score += 100
                        if not config.has_key and not config.key_pos and random.random() < 0.5:
                            config.key_pos = (atk_x, atk_y)
