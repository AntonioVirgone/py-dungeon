import random
from collections import deque


def genera_mappa(dim=10):
    # Crea una mappa piena di 0 (muri)
    mappa = [[0] * dim for _ in range(dim)]

    # Funzione per garantire che ci sia un percorso tra (1, 1) e (dim-2, dim-2)
    def crea_percorso():
        # Iniziamo il percorso dal punto (1, 1) al punto (dim-2, dim-2)
        start = (1, 1)
        end = (dim - 2, dim - 2)

        # BFS per trovare un percorso
        queue = deque([start])
        parent = {start: None}
        directions = [(0, 1), (1, 0)]

        while queue:
            current = queue.popleft()
            if current == end:
                break
            for direction in directions:
                next_cell = (current[0] + direction[0], current[1] + direction[1])
                if 1 <= next_cell[0] < dim - 1 and 1 <= next_cell[1] < dim - 1 and next_cell not in parent:
                    queue.append(next_cell)
                    parent[next_cell] = current

        # Ricostruiamo il percorso dal punto finale al punto di partenza
        current = end
        while current != start:
            mappa[current[0]][current[1]] = 1  # Percorso libero
            current = parent[current]
        mappa[start[0]][start[1]] = 1  # Assicura che la partenza sia libera

    # Funzione per aggiungere muri in modo casuale, evitando di bloccare il percorso
    def aggiungi_muri():
        for x in range(1, dim - 1):
            for y in range(1, dim - 1):
                if mappa[x][y] == 0 and random.random() > 0.5:
                    # Aggiungi muri in posizioni casuali ma non sui percorsi
                    if mappa[x][y] == 0:
                        mappa[x][y] = 1

    # Creiamo il percorso garantito
    crea_percorso()

    # Aggiungiamo muri in modo casuale, ma senza bloccare il percorso
    aggiungi_muri()

    return mappa


# Funzione per stampare la mappa in modo leggibile
def stampa_mappa(mappa):
    for riga in mappa:
        print(" ".join(map(str, riga)))


# Genera e stampa la mappa 10x10
mappa = genera_mappa()
stampa_mappa(mappa)


def is_cell_empty(x,y):
    if mappa[x][y] == 1:
        return True