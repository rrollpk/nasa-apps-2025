import rasterio
import geopandas as gpd
import pandas as pd
from rasterio.mask import mask

# 1️⃣ Abrir el archivo tif
tif_path = "pm25_avg24_int.tif"
src = rasterio.open(tif_path)

# 2️⃣ Abrir el shapefile de España (puede ser provincias, comunidades o frontera del país)
spain_shp = "spain_boundary.shp"  # reemplaza con tu shapefile
spain = gpd.read_file(spain_shp)

# 3️⃣ Recortar el raster a España
out_image, out_transform = mask(src, spain.geometry, crop=True)
out_image = out_image[0]  # asumimos 1 banda

# 4️⃣ Generar coordenadas de cada celda
rows, cols = out_image.shape
xs, ys = rasterio.transform.xy(out_transform, 
                               row=list(range(rows)), 
                               col=list(range(cols)), 
                               offset='center')

import numpy as np
xs = np.array(xs)
ys = np.array(ys)

# Necesitamos hacer meshgrid para todas las combinaciones
xx, yy = np.meshgrid(xs, ys)
values = out_image.flatten()
xx = xx.flatten()
yy = yy.flatten()

# 5️⃣ Crear DataFrame solo con valores válidos
valid_mask = values != src.nodata
df = pd.DataFrame({
    "x": xx[valid_mask],
    "y": yy[valid_mask],
    "pm25": values[valid_mask]
})

# 6️⃣ Guardar a CSV
df.to_csv("pm25_spain.csv", index=False)
print("✅ CSV generado con datos válidos de España")
