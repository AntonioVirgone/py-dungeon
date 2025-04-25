import random


def genera_mappa(dim=10):
    # Crea una mappa piena di 0 (muri)
    mappa = [[0] * dim for _ in range(dim)]

    # Funzione per dividere la mappa e generare il labirinto
    def dividi_labirinto(x1, y1, x2, y2):
        # Condizione di fermata per la ricorsione: se la sezione è troppo piccola, non dividere
        if x2 - x1 < 2 or y2 - y1 < 2:
            return

        # Decidere se dividere orizzontalmente o verticalmente
        if (x2 - x1) > (y2 - y1):
            # Divisione verticale
            if x2 - x1 > 2:
                mx = random.randint(x1 + 1, x2 - 2)  # Evita di prendere un range vuoto
                for i in range(y1, y2):
                    mappa[mx][i] = 1  # Aggiungi muro verticale
                # Crea un passaggio nel muro
                mappa[mx][random.randint(y1, y2 - 1)] = 0

                # Dividi la mappa in due parti
                dividi_labirinto(x1, y1, mx, y2)
                dividi_labirinto(mx + 1, y1, x2, y2)
        else:
            # Divisione orizzontale
            if y2 - y1 > 2:
                my = random.randint(y1 + 1, y2 - 2)  # Evita di prendere un range vuoto
                for i in range(x1, x2):
                    mappa[i][my] = 1  # Aggiungi muro orizzontale
                # Crea un passaggio nel muro
                mappa[random.randint(x1, x2 - 1)][my] = 0

                # Dividi la mappa in due parti
                dividi_labirinto(x1, y1, x2, my)
                dividi_labirinto(x1, my + 1, x2, y2)

    # Inizia la divisione ricorsiva sulla mappa
    dividi_labirinto(1, 1, dim - 2, dim - 2)

    # Assicuriamoci che ci sia sempre un percorso valido
    mappa[1][1] = 0  # Punto di partenza
    mappa[dim - 2][dim - 2] = 0  # Punto finale

    return mappa


# Funzione per stampare la mappa in modo leggibile
def stampa_mappa(mappa):
    for riga in mappa:
        print(" ".join(map(str, riga)))


# Genera e stampa la mappa 10x10
mappa = genera_mappa()
stampa_mappa(mappa)
