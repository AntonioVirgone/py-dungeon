# Mappa (0 = muro, 1 = pavimento)
import random


def genera_mappa(dim=10):
    # Crea una mappa di dimensione dim x dim
    # Prima riga costante con tutti i valori a 0
    mappa = [[0] * dim]

    for _ in range(1, dim-1):
        # Ogni riga della mappa è una lista con valori casuali tra 0 e 1
        riga = [0] + [random.randint(0, 1) for _ in range(dim - 2)] + [0]
        mappa.append(riga)

    # Ultima riga costante con tutti i valori a 0
    mappa.append([0] * dim)

    return mappa


# Funzione per stampare la mappa in modo leggibile
def stampa_mappa(mappa):
    for riga in mappa:
        print(" ".join(map(str, riga)))


# Genera e stampa la mappa 10x10
game_map = genera_mappa()
stampa_mappa(game_map)
