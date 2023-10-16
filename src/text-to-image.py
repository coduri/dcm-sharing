import math
import numpy as np
from PIL import Image


# Funzione di encoding: trasforma una stringa in immagine in scala di grigi
def string_to_grayscale_image(input_string, output_file):
    # Converte ogni carattere della stringa nel suo valore ASCII
    pixel_values = [ord(char) for char in input_string]
    input_length = len(input_string)

    # Crea un'immagine quadrata vuota
    image_size = int(math.ceil(math.sqrt(input_length)))
    grayscale_image = Image.new("L", (image_size, image_size))

    # Carica i pixel e salva l'immagine
    grayscale_image.putdata(pixel_values)
    grayscale_image.save(output_file)

    # Converte l'immagine in un array np e lo restituisce
    grayscale_array = np.array(grayscale_image).astype(int)

    return grayscale_array


# Funzione di decoding: trasforma l'immagine in scala di grigi nella corrispondente stringa
def grayscale_image_to_string(input_file):
    # Recupero pixel con valori ASCII "significativi"
    grayscale_image = Image.open(input_file)
    pixel_values = list(grayscale_image.getdata())
    meaningful_pixels = [pixel for pixel in pixel_values if pixel >= 32]

    # Converto valori in caratteri e creo stringa
    char_values = [chr(pixel) for pixel in meaningful_pixels]
    decoded_string = ''.join(char_values)

    return decoded_string
