from PIL import Image


# Funzione che restituisce l'immagine monocromatica sul canale indicato
def zero_other_channels(image, channel):
    zeroed_image = Image.new("CMYK", image.size)

    for y in range(image.size[1]):
        for x in range(image.size[0]):
            pixel = list(image.getpixel((x, y)))

            for c in range(3):
                if c != channel:
                    pixel[c] = 0

            zeroed_image.putpixel((x, y), tuple(pixel))

    return zeroed_image


# Funzione che implementa l'algoritmo dithering di Floyd-Steinberg
def floyd_steinberg_dithering(img, channel):
    dithered_image = Image.new("CMYK", img.size)

    for y in range(img.size[1]):  # altezza
        for x in range(img.size[0]):  # larghezza
            pixel = list(img.getpixel((x, y)))
            old_value = pixel[channel]

            pixel[channel] = 255 if pixel[channel] > 128 else 0
            new_value = pixel[channel]

            dithered_image.putpixel((x, y), tuple(pixel))

            quant_error = old_value - new_value

            # Parte di Error Diffusion (+ controlli sui pixel ai bordi)
            if x < img.size[0] - 1:
                pixel = list(img.getpixel((x + 1, y)))
                pixel[channel] += quant_error * 7 // 16
                img.putpixel((x + 1, y), tuple(pixel))

                if y < img.size[1] - 1:
                    pixel = list(img.getpixel((x + 1, y + 1)))
                    pixel[channel] += quant_error * 1 // 16
                    img.putpixel((x + 1, y + 1), tuple(pixel))

            if y < img.size[1] - 1:
                pixel = list(img.getpixel((x, y + 1)))
                pixel[channel] += quant_error * 5 // 16
                img.putpixel((x, y + 1), tuple(pixel))

                if x > 0:
                    pixel = list(img.getpixel((x - 1, y + 1)))
                    pixel[channel] += quant_error * 3 // 16
                    img.putpixel((x - 1, y + 1), tuple(pixel))

    return dithered_image


# Funzione che prende tutte le immagini monocromatiche halftoned e le unisce
def merge_dithered_images(cyan_image, magenta_image, yellow_image):
    assert cyan_image.size == magenta_image.size == yellow_image.size, "Le dimensioni delle immagini dithered non corrispondono"
    combined_image = Image.new("CMYK", cyan_image.size)

    for y in range(cyan_image.size[1]):
        for x in range(cyan_image.size[0]):
            cyan_value = cyan_image.getpixel((x, y))[0]
            magenta_value = magenta_image.getpixel((x, y))[1]
            yellow_value = yellow_image.getpixel((x, y))[2]

            pixel = (cyan_value, magenta_value, yellow_value, 0)
            combined_image.putpixel((x, y), pixel)

    return combined_image
