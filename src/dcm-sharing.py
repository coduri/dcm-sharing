#!/usr/bin/env python3

import argparse
import sys
from argparse import RawTextHelpFormatter

from Encrypt import *
from Decrypt import *
from Reconstruct import *


# Funzione che verifica l'esistenza delle cartelle indicate
def check_folder_existence(path):
    return os.path.exists(path) and os.path.isdir(path)


# Creo parser
parser = argparse.ArgumentParser(usage=argparse.SUPPRESS, formatter_class=RawTextHelpFormatter)

# Aggiungo descrizione personalizzata all'helper
custom_help = """
DICOM Image Encryptor/Decryptor

Syntax for encryption:
    ./dcm-sharing.py -e -m <partial | all> -ef <txt | json> -f <DICOM FILE> -o <FOLDER>

Syntax for decription:
    ./dcm-sharing -d -m <partial | all> -ef <txt | json> -i <FOLDER>
    
If you want to ensure that the DICOM file is reconstructable during decryption, you must set the options '-m all' and '-ef json' both when encrypting and decrypting. 
"""

parser.description = custom_help

# Modalità
parser.add_argument("-e", "--encrypt", help="Encrypt a DICOM file", action="store_true")
parser.add_argument("-d", "--decrypt", help="Decrypt a DICOM file", action="store_true")

# Argomenti comuni
parser.add_argument("-m", "--metadata", choices=["all", "partial"], required=True, help="When set to 'partial', only pixel data and PHI reconstruction is possible. When set to 'all', full DICOM file reconstruction is possible (required).")
parser.add_argument("-ef", "--encoding-format", choices=["json", "txt"], required=True, help="Desired encoding format for metadata (required).")

# Argomenti per la cifratura
parser.add_argument("-f", "--file", help="Path to the DICOM file (required for encryption)")
parser.add_argument("-o", "--output-folder", help="Path to the output folder for results (required for encryption)")

# Argomenti per la decifratura
parser.add_argument("-i", "--input-folder", help="Path to the folder containing random grids (required for decryption)")

# Parsing argomenti
args = parser.parse_args()


# Controllo gli argomenti
if args.encrypt and args.decrypt:
    print("Error: Specify a unique action to perform (-e for encryption, -d for decryption).")

elif args.encrypt:
    if args.file and args.output_folder and args.metadata and args.encoding_format:

        if check_folder_existence(args.output_folder) is True:
            print("Encrypting DICOM file...")

            if encrypt(args.file, args.metadata, args.encoding_format, args.output_folder) is None:
                sys.exit()
            else:
                print("Encryption completed.")

        else:
            print(f"Error: The path '{args.output_folder}' does not exist or is not a valid folder.")

    else:
        print("Error: For encryption, you must specify -m (metadata), "
              "-ef (encoding format), -f (file) and -o (output folder) options.")

elif args.decrypt:
    if args.input_folder and args.metadata and args.encoding_format:

        if check_folder_existence(args.input_folder) is True:
            print("Decrypting DICOM file...")

            if decrypt(args.input_folder, args.metadata, args.encoding_format) is None:
                sys.exit()
            else:
                print("Decryption completed.")

            # Se modalità 'all metadata' con encoding 'json' ho a disposizione tutti i file per ricostruire
            if args.metadata == 'all' and args.encoding_format == 'json':
                print("Reconstructing DICOM file...")

                if reconstruction(args.input_folder) is None:
                    sys.exit()
                else:
                    print("Reconstruction completed.")

        else:
            print(f"Error: The path '{args.output_folder}' does not exist or is not a valid folder.")

    else:
        print("Error: For decryption, you must specify -m (metadata), -ef (encoding format) "
              "and -i (input folder) options.")

else:
    print("Error: Specify a valid action to perform (-e for encryption, -d for decryption).")
