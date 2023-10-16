import numpy as np


# Funzione che crea una random grid della dimensione specificata
def create_first_random_grid(size):
    grid = np.random.randint(2, size=size)
    return grid


# Funzione che crea la seconda random grid secondo la prima equazione di Kafri e Keren
def create_second_random_grid(image, grid):
    transformed_grid = np.where(image == 0, grid, 1 - grid)
    return transformed_grid


# Funzione che sovrappone le due grid con XOR
def overlay_images_XOR(image1, image2):
    overlaid_image = np.bitwise_xor(image1, image2)
    overlaid_image = 1 - overlaid_image
    return overlaid_image


# Funzione che sovrappone le due grid con OR
def overlay_images_OR(image1, image2):
    overlaid_image = np.bitwise_or(image1, image2)
    overlaid_image = 1 - overlaid_image
    return overlaid_image
