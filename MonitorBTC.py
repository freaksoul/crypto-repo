import pandas as pd
import requests
import csv
from datetime import datetime
import matplotlib.pyplot as plt

# Configuración
CSV_PRECIOS = "C:\\Viboron\\CryptoProyecto\\BTC_precios.csv"
LOG_FILE = "C:\\Viboron\\CryptoProyecto\\BTC_decisiones.csv"

# Leer precios históricos
df = pd.read_csv(CSV_PRECIOS, names=["fecha", "precio"], parse_dates=["fecha"])
df.sort_values("fecha", inplace=True)

# Calcular umbral dinámico
media = df["precio"].tail(30).mean()
std = df["precio"].tail(30).std()
umbral_compra = media - std
print(f"🎯 Umbral de compra dinámico: ${umbral_compra:,.0f} MXN")

# Obtener precio actual desde Bitso
def get_btc_price():
    url = "https://api.bitso.com/v3/ticker/?book=btc_mxn"
    response = requests.get(url)
    data = response.json()
    return float(data['payload']['last'])

# Registrar decisión
def log_decision(price, decision):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, price, decision])
    print(f"📝 Registrado: {timestamp} | ${price:,.0f} MXN | {decision}")

# Evaluar y alertar
def evaluar():
    price = get_btc_price()
    print(f"📈 Precio actual BTC: ${price:,.0f} MXN")

    if price <= umbral_compra:
        log_decision(price, "Comprar")
    elif price >= media + std:
        log_decision(price, "Vender")
    else:
        log_decision(price, "Mantener")

# Visualizar historial
def graficar_historial():
    df_log = pd.read_csv(LOG_FILE, names=["Fecha", "Precio", "Decision"])
    df_log["Fecha"] = pd.to_datetime(df_log["Fecha"])

    plt.figure(figsize=(10,6))
    plt.plot(df_log["Fecha"], df_log["Precio"], label="Precio BTC", marker='o')
    for i in range(len(df_log)):
        plt.text(df_log["Fecha"][i], df_log["Precio"][i], df_log["Decision"][i], fontsize=8)

    plt.axhline(umbral_compra, color='green', linestyle='--', label="Umbral Compra")
    plt.axhline(media + std, color='red', linestyle='--', label="Umbral Venta")

    plt.title("Historial de precios y decisiones BTC")
    plt.xlabel("Fecha")
    plt.ylabel("Precio (MXN)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Ejecutar
evaluar()
graficar_historial()
