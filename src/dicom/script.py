from pydicom import dcmread
from src.dicom.functions import *

# dcmread: legge file DICOM e resituisce un Dataset
pathDICOM = '../../resources/file.dcm'
DICOM_file = dcmread(pathDICOM)

# Effettuo una conversione dell'immagine DICOM in PNG e la salvo
from_DataPixel_to_PNG(DICOM_file.pixel_array, '../../resources/output/dicom/converted.png')

# Stampo i metadati considerati sensibili
sensitive_metadata = get_sensitive_metadata(DICOM_file)
print(sensitive_metadata)
