import pandas as pd

df = pd.read_csv("C:\\Viboron\\BTC_precios.csv", parse_dates=["fecha"])
#df = pd.read_csv("C:\\Viboron\\TUSD_precios.csv", parse_dates=["fecha"])
df.sort_values("fecha", inplace=True)

# Promedio móvil de los últimos 7 días
precio_promedio = df["precio"].tail(7).mean()
print(f"📊 Precio promedio últimos 7 días: ${precio_promedio:,.0f} MXN")

precio_minimo = df["precio"].tail(30).min()
print(f"📉 Precio mínimo últimos 30 días: ${precio_minimo:,.0f} MXN")

std = df["precio"].tail(30).std()
media = df["precio"].tail(30).mean()
umbral_compra = media - std
print(f"🎯 Umbral de compra sugerido: ${umbral_compra:,.0f} MXN")

