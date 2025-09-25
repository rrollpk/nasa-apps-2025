# Instala gdown si no lo tienes
# pip install gdown

import gdown


url = f"https://drive.google.com/uc?id=1morNbC-l4O1P_6-Q-7Iq1z5WliMmeRGv"
output = "pm25_avg24_int.tif"

gdown.download(url, output, quiet=False)
