import numpy as np


# Funzione che crea la prima random grid con valori casuali nel range (0-255)
def create_random_grid(size):
    grid = np.random.randint(0, 256, size=size)
    return grid


# Funzione che crea la seconda random grid
def create_difference_grid(image, grid):
    transformed_grid = grid - image
    return transformed_grid


# Funzione che "sovrappone" le due random grid
def overlay_grids(image1, image2):
    overlaid_image = image1 - image2
    return overlaid_image

