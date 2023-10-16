# Terminatore del messagio segreto
DELIMITER = '$$$'


# Funzione che converte una stringa di caratteri in una stringa binaria
def from_string_to_bin(string):
    return ''.join([format(ord(c), "08b") for c in string])


# Funzione che dato un messaggio e un oggetto di copertura applica steganografia LSB
def encode(img_array, message):
    # Aggiungo terminatore alla fine del messaggio segreto e converto in binario
    message += DELIMITER
    binary_message = from_string_to_bin(message)

    # Variabile che permette di ricostruire la cover-image nella fase di decodifica
    lsb_recovery = []

    # Calcolo dimensioni
    required_pixels = len(binary_message)
    # print("Pixel richiesti: ", required_pixels, "\t Pixel disponibili: ", img_array.size)
    if required_pixels > img_array.size:
        return None, None

    # Applico steganografia
    else:
        index = 0

        for i in range(img_array.shape[0]):
            for j in range(img_array.shape[1]):

                if index < required_pixels:
                    # Salvo bit che verrà sostituito per eventuale recovery
                    lsb = img_array[i][j] & 1
                    lsb_recovery.append(lsb)

                    # Sostituisco l'ultimo bit del pixel con un bit di segreto
                    img_array[i][j] = (int(img_array[i][j]) & 0xFE) | int(binary_message[index])
                    index += 1

                else:
                    break

        return img_array, lsb_recovery


# Funzione che converte una stringa binaria in una stringa di caratteri
def from_bin_to_string(bin):
    return ''.join([chr(int(bin[k:k + 8], 2)) for k in range(0, len(bin), 8)])


# Funzione che riceve uno stego-object e restituisce il segreto.
# Se gli viene fornito l'array lsb_recovery restituisce anche il cover-obj ricostruito
def decode(img_array, lsb_recovery=None):
    hidden_bits = ""
    complete_secret = False
    index = 0

    delimiter_binary = ''.join(format(ord(c), '08b') for c in DELIMITER)
    delimiter_length = len(delimiter_binary)

    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            # Recupero bit di segreto
            pixel_lsb = img_array[i][j] & 1
            hidden_bits += str(pixel_lsb)

            # Se c'è a disposizione lsb_recovery => steganografia reversibile
            if lsb_recovery is not None:
                img_array[i][j] = (int(img_array[i][j]) & 0xFE) | lsb_recovery[index]
                index += 1

            # Se ho letto la stringa di terminazione completa
            if hidden_bits[-delimiter_length:] == delimiter_binary:
                # Rimuovo tale stringa dal segreto ed esco dai due for
                hidden_bits = hidden_bits[:-delimiter_length]
                complete_secret = True
                break

        if complete_secret:
            break

    # Restituisco la stringa di segreto e se presente anche la cover image
    if complete_secret:
        if lsb_recovery is not None:
            return from_bin_to_string(hidden_bits), img_array
        else:
            return from_bin_to_string(hidden_bits), None
    else:
        return None, None
