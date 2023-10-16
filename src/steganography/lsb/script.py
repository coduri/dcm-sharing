import numpy as np
from PIL import Image
from src.steganography.lsb.functions import *

# Apro e converto cover image in scala di grigi e poi in np.array
cover_image = Image.open("../../../resources/secret.jpg").convert('L')
cover_array = np.array(cover_image)


# Faccio encoding e salvo stego-image
message = 'Messaggio segreto di Christian'
stego_array, lsb_array = encode(cover_array, message)

if stego_array is not None:
    stego_image = Image.fromarray(stego_array.astype('uint8'))
    stego_image.save("../../../resources/output/lsb/stego_image.png")


# Faccio decoding e stampo messaggio segreto
secret, _ = decode(stego_array)

if secret is not None:
    print(secret)

"""
Se volessi ottenere una steganografia reversibile, è sufficiente passare lsb_array alla funzione decode().
In tale caso mi verrebbe restiuito, come secondo parametro un recovered_array che sarà identico al cover_array
"""
