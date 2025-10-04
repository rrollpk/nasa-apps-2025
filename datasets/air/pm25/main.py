import pandas as pd
import numpy as np

def media_winsorizada_superior(series, ventana, percentil_superior=0.9):
    """
    Media winsorizada que solo recorta valores extremos superiores
    Útil para datos como incendios donde los valores muy altos sesgan la muestra
    """
    def winsorize_upper_mean(x):
       
        
        # Calcular solo el límite superior (percentil 90 por defecto)
        limite_sup = x.quantile(percentil_superior)
        
        # Winsorizar solo por arriba (clip upper)
        x_winsorizado = x.clip(upper=limite_sup)
        
        return x_winsorizado.mean()
    
    return series.rolling(window=ventana).apply(winsorize_upper_mean)

# Ejemplo con datos simulados de incendios
# (valores normales bajos con algunos picos extremos)
datos_incendios = pd.Series([
    5, 8, 12, 7, 10, 15, 200,  # <- valor extremo (incendio grande)
    9, 11, 6, 14, 8, 500,      # <- valor extremo 
    7, 12, 9, 15, 11, 8, 13, 
    10, 7, 300, 12, 9          # <- valor extremo
])

# Comparar media normal vs winsorizada superior
ventana = 7
percentil = 0.8  # Recorta el 20% superior

media_normal = datos_incendios.rolling(window=ventana).mean()
media_winsorizada = media_winsorizada_superior(datos_incendios, ventana, percentil)

# Crear DataFrame para comparar
comparacion = pd.DataFrame({
    'datos_originales': datos_incendios,
    'media_normal': media_normal,
    'media_winsorizada': media_winsorizada
})

print(comparacion.round(2))

