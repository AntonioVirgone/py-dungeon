import random

def generate_random_level(width=10, height=10, walk_length=50, num_enemies=3, seed=None):
    if seed is not None:
        random.seed(seed)

    # Inizializza la mappa piena di muri (0)
    dungeon = [[0 for _ in range(width)] for _ in range(height)]

    # Partenza: centro della mappa
    x, y = width // 2, height // 2
    dungeon[y][x] = 1
    visited = [(x, y)]

    # Random walk per creare il dungeon
    for _ in range(walk_length):
        dx, dy = random.choice([(0,1), (0,-1), (1,0), (-1,0)])
        nx, ny = x + dx, y + dy
        if 1 <= nx < width-1 and 1 <= ny < height-1:
            x, y = nx, ny
            dungeon[ny][nx] = 1
            visited.append((nx, ny))

    # Posizionamento del giocatore
    player_start = visited[0]

    # Posizione chiave: lontana almeno 5 caselle
    far_tiles = [pos for pos in visited if abs(pos[0] - player_start[0]) + abs(pos[1] - player_start[1]) > 5]
    key_pos = random.choice(far_tiles) if far_tiles else random.choice(visited)

    # Posizionamento nemici
    possible_enemies = [pos for pos in visited if pos != player_start and pos != key_pos]
    enemy_positions = random.sample(possible_enemies, min(num_enemies, len(possible_enemies)))

    return {
        "map": dungeon,
        "player_start": player_start,
        "key": key_pos,
        "enemies": enemy_positions
    }
