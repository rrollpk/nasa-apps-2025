import rasterio

# Ruta al archivo .tif (ajústala según dónde lo tengas)
tif_path = "pm25_avg24_int.tif"

# Abrir el archivo
with rasterio.open(tif_path) as src:
    print("📂 Información del archivo:")
    print("-------------------------")
    print("Número de bandas:", src.count)
    print("Dimensiones (alto, ancho):", src.height, "x", src.width)
    print("Sistema de coordenadas:", src.crs)
    print("Transformación (origen y resolución):", src.transform)


    print("\nmetadatos")
    print(src.meta)

    # Ejemplo: acceder a la primera banda
    band1 = src.read(1)  # lee la banda 1 como array de numpy
    print("\n data:")
    print("Tipo de datos:", band1.dtype)
    print("Forma:", band1.shape)
    print("Valor mínimo:", band1.min())
    print("Valor máximo:", band1.max())
