from level import bfs


class Enemy:
    def __init__(self, config):
        self.config = config


    def move(self, frame_count):
        if not self.config.game_over and not self.config.level_complete and frame_count % self.config.ENEMY_MOVE_DELAY == 0:
            new_enemies = []
            for ex, ey in self.config.enemies:
                path = bfs((ex, ey), (self.config.player.player_x, self.config.player.player_y), self.config.game_map, self.config.enemies)
                if path:
                    next_step = path[0]
                    if next_step == (self.config.player.player_x, self.config.player.player_y):
                        self.config.player.player_lives -= 1
                        if self.config.player.player_lives <= 0:
                            self.config.game_over = True
                    else:
                        new_enemies.append(next_step)
                else:
                    new_enemies.append((ex, ey))
            self.config.enemies = new_enemies