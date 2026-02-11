import pandas as pd

# Cargar precios históricos
df = pd.read_csv("C:\\Viboron\\TUSD_precios.csv", names=["fecha", "precio"], parse_dates=["fecha"])
df.sort_values("fecha", inplace=True)

# Promedio móvil de los últimos 7 días
precio_promedio = df["precio"].tail(7).mean()
print(f"📊 Precio promedio últimos 7 días: ${precio_promedio:,.2f} MXN")

# Precio mínimo de los últimos 30 días
precio_minimo = df["precio"].tail(30).min()
print(f"📉 Precio mínimo últimos 30 días: ${precio_minimo:,.2f} MXN")

# Umbral de venta sugerido
std = df["precio"].tail(30).std()
media = df["precio"].tail(30).mean()
umbral_venta = media + std
print(f"💰 Umbral de venta sugerido: ${umbral_venta:,.2f} MXN")