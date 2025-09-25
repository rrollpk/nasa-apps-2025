import xml.etree.ElementTree as ET
import rasterio
import numpy as np

tree = ET.parse('72a465a6-4af1-4b0c-ade5-ddfa23cc19fe.xml')
root = tree.getroot()

# Acceder a los elementos del XML
for child in root:
    print(child.tag, child.attrib)

with rasterio.open("pm25_avg24_int.tif") as src:
    data = src.read(1)       
    profile = src.profile   


print(data.shape, data.min(), data.max())
