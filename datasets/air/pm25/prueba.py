import pandas as pd
import numpy as np

pm25 = pd.Series([
    5, 8, 12, 7, 10, 15, 200,  # <- valor extremo (incendio grande)
    9, 11, 6, 14, 8, 500,      # <- valor extremo 
    7, 12, 9, 15, 11, 8, 13, 
    10, 7, 300, 12, 9          # <- valor extremo
])

def winsorized_upper_mean(x):
   
    limite_sup = x.quantile(0.9)        
    x_winsorizado = x.clip(upper=limite_sup)  

    return x_winsorizado.mean()         

# Función principal
def media_winsorizada_superior(series, window, percentil_superior=0.9):
    def winsorize_upper_mean(x):
        limite_sup = x.quantile(percentil_superior)
        x_winsorizado = x.clip(upper=limite_sup)
        return x_winsorizado.mean()
    
    return series.rolling(window).apply(winsorize_upper_mean)

# Parámetros
window = 3
media_normal = pm25.rolling(window).mean()
media_winsorizada = media_winsorizada_superior(pm25, window)

print("Datos originales:")
print(pm25.values)
print("\nMedia normal:")
print(media_normal.round(2))
print("\nMedia winsorizada:")
print(media_winsorizada.round(2))

# Comparación
comparacion = pd.DataFrame({
    'original': pm25,
    'media_normal': media_normal,
    'media_winsorizada': media_winsorizada
})

print("\nComparing:")
print(comparacion.round(2))