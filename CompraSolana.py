import pandas as pd
import requests

# === CARGAR PRECIOS HISTÓRICOS ===
df_sol = pd.read_csv("C:\\Viboron\\SOL_precios.csv", names=["fecha", "precio"], parse_dates=["fecha"])
df_eth = pd.read_csv("C:\\Viboron\\ETH_precios.csv", names=["fecha", "precio"], parse_dates=["fecha"])
df_sol.sort_values("fecha", inplace=True)
df_eth.sort_values("fecha", inplace=True)

# === FUNCIONES DE ANÁLISIS ===
def calcular_umbral(df, nombre):
    media = df["precio"].tail(30).mean()
    std = df["precio"].tail(30).std()
    umbral_compra = media - std

    print(f"🎯 Umbral de compra sugerido para {nombre}: ${umbral_compra:,.2f} USD")
    return umbral_compra

def obtener_precio_actual(moneda):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={moneda}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return float(data[moneda]["usd"])

def evaluar_compra(moneda, umbral):
    precio_actual = obtener_precio_actual(moneda)
    print(f"📈 Precio actual de {moneda.upper()}: ${precio_actual:.2f} USD")
    if precio_actual <= umbral:
        print(f"✅ Buen momento para comprar {moneda.upper()}.")
    else:
        print(f"⏳ Aún no conviene comprar {moneda.upper()}.")

# === EJECUCIÓN ===
umbral_sol = calcular_umbral(df_sol, "Solana")
umbral_eth = calcular_umbral(df_eth, "Ethereum")

evaluar_compra("solana", umbral_sol)
evaluar_compra("ethereum", umbral_eth)