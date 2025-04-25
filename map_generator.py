import random


def genera_mappa(dim=10):
    # Crea una mappa di dimensione dim x dim con il bordo esterno a 0
    mappa = [[0] * dim for _ in range(dim)]

    # Funzione per generare un percorso valido
    def crea_percorso(x, y, fine_x, fine_y):
        # Direzioni in cui possiamo muoverci: sopra, sotto, sinistra, destra
        direzioni = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        stack = [(x, y)]
        percorso = set()  # Set per evitare duplicati
        percorso.add((x, y))

        while stack:
            cx, cy = stack[-1]

            if (cx, cy) == (fine_x, fine_y):
                break

            # Mescola le direzioni per evitare percorsi lineari
            random.shuffle(direzioni)
            trovato = False

            for dx, dy in direzioni:
                nx, ny = cx + dx, cy + dy

                # Verifica che la nuova posizione sia valida e non visitata
                if 0 < nx < dim - 1 and 0 < ny < dim - 1 and (nx, ny) not in percorso:
                    stack.append((nx, ny))
                    percorso.add((nx, ny))
                    trovato = True
                    break

            # Se non è stato trovato nessun percorso valido, torniamo indietro
            if not trovato:
                stack.pop()

        # Segna tutte le celle del percorso con 1
        for (px, py) in percorso:
            mappa[px][py] = 1

    # Crea un percorso tra (1, 1) e (dim-2, dim-2)
    crea_percorso(1, 1, dim - 2, dim - 2)

    # Riempi il resto della mappa con 0 e 1 casuali, evitando di bloccare il percorso
    for i in range(1, dim - 1):
        for j in range(1, dim - 1):
            if mappa[i][j] != 1:  # Se la cella non fa parte del percorso
                mappa[i][j] = random.choice([0, 1])

    return mappa


# Funzione per stampare la mappa in modo leggibile
def stampa_mappa(mappa):
    for riga in mappa:
        print(" ".join(map(str, riga)))


# Genera e stampa la mappa 10x10
mappa = genera_mappa()
stampa_mappa(mappa)
