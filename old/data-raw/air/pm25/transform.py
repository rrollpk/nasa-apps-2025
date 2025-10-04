import rasterio
import pandas as pd
import numpy as np

# Ruta al archivo TIF
tif_path = "pm25_avg24_int.tif"

# Abrir el archivo raster
with rasterio.open(tif_path) as src:
    band = src.read(1)  # primera banda (PM2.5)
    transform = src.transform
    
    # Crear arrays de coordenadas (x, y) para cada píxel
    rows, cols = np.meshgrid(np.arange(band.shape[0]), np.arange(band.shape[1]), indexing="ij")
    xs, ys = rasterio.transform.xy(transform, rows, cols)
    
    # Aplanar a 1D
    xs = np.array(xs).flatten()
    ys = np.array(ys).flatten()
    values = band.flatten()

# Filtrar valores nulos (nodata = -3.4028235e+38)
nodata = src.nodata
mask = values != nodata

df = pd.DataFrame({
    "x": xs[mask],
    "y": ys[mask],
    "pm25": values[mask]
})

print(df.head())
print(f"Total filas: {len(df)}")

# Guardar como CSV para la base de datos
df.to_csv("pm25_points.csv", index=False)

