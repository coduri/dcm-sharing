import numpy as np


# Funzione che restituisce un array di bitplane
def slice_bit_plane(img, num_planes):
    bit_planes = []
    img_array = np.array(img)

    for i in range(num_planes - 1, -1, -1):
        # Estraggo il bit i-esimo e lo aggiungo alla bitplane
        bit_i = (img_array >> i) & 1
        bit_planes.append(bit_i)

    return bit_planes
