import pandas as pd

df = pd.read_csv("pm25_points.csv")
print(df.head())
print("📋 Columnas:", df.columns.tolist())
