import pandas as pd
import matplotlib.pyplot as plt

# Cargar el archivo CSV
df = pd.read_csv("C:\\Viboron\\CryptoProyecto\\bitcoin_precios.csv", names=["Fecha", "Precio"])

# Convertir la columna de fecha a tipo datetime
df["Fecha"] = pd.to_datetime(df["Fecha"])

# Graficar
plt.figure(figsize=(10, 5))
plt.plot(df["Fecha"], df["Precio"], marker='o', linestyle='-', color='orange')
plt.title("Precio de Bitcoin en Bitso")
plt.xlabel("Fecha")
plt.ylabel("Precio en MXN")
plt.grid(True)
plt.tight_layout()
plt.show()