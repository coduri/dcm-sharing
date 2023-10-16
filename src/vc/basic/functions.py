import random
import copy


# Funzione che mappa il valore: dalla codifica RGB allo standard VC
def map_rgb_to_bit(rgb_value):
    if rgb_value == 0:
        return 1
    if rgb_value == 255:
        return 0


# Funzione che mappa il valore: dallo standard VC alla codifica RGB
def map_bit_to_rgb(vc_value):
    if vc_value == 1:
        return 0
    if vc_value == 0:
        return 255


# Funzione che permuta sulla colonna, in modo casuale, la matrice fornita
def random_col_permutation(matrix):
    n_rows = len(matrix)
    n_cols = len(matrix[0])
    new_matrix = copy.deepcopy(matrix)

    # Lista contenente gli indici delle colonne della matrice originale
    col_indices = list(range(n_cols))

    # Mischio in modo casuale gli elementi della lista
    random.shuffle(col_indices)

    # Creo una matrice con le colonne mischiate
    for i in range(n_rows):
        for j in range(n_cols):
            new_matrix[i][j] = matrix[i][col_indices[j]]

    return new_matrix


# Funzione che popola i subpixel degli share in base alla matrice ricevuta
def populate_subpixels(share1, share2, i, j, matrix):
    # Popolo subpixel Share1
    share1.putpixel((i * 2, j * 2), matrix[0][0])
    share1.putpixel((i * 2, j * 2 + 1), matrix[0][1])
    share1.putpixel((i * 2 + 1, j * 2), matrix[0][2])
    share1.putpixel((i * 2 + 1, j * 2 + 1), matrix[0][3])

    # Popolo subpixel Share2
    share2.putpixel((i * 2, j * 2), matrix[1][0])
    share2.putpixel((i * 2, j * 2 + 1), matrix[1][1])
    share2.putpixel((i * 2 + 1, j * 2), matrix[1][2])
    share2.putpixel((i * 2 + 1, j * 2 + 1), matrix[1][3])
