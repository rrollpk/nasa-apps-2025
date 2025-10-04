import psycopg2

DB_URL = "postgresql://postgres:iPZuSfQGnhCgkeTwjyTxHdglDoJLubeu@crossover.proxy.rlwy.net:35753/railway"

conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

# Crear tabla (ajusta tipos)
cur.execute("""
CREATE TABLE IF NOT EXISTS pm25_data (
    lon FLOAT,
    lat FLOAT,
    value FLOAT
);
""")
conn.commit()

# Cargar CSV directamente en la tabla
with open("pm25_points.csv", "r", encoding="utf-8") as f:
    next(f)  # saltar encabezado
    cur.copy_from(f, "pm25_data", sep=",", columns=("lon","lat","value"))

conn.commit()
cur.close()
conn.close()

print("✅ Datos cargados con COPY (mucho más rápido)")
