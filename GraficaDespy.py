import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("C:\\Viboron\\btc_decisiones.csv", names=["Fecha", "Precio", "Decision"])
df["Fecha"] = pd.to_datetime(df["Fecha"])

plt.figure(figsize=(10,6))
plt.plot(df["Fecha"], df["Precio"], label="Precio BTC", marker='o')
for i in range(len(df)):
    plt.text(df["Fecha"][i], df["Precio"][i], df["Decision"][i], fontsize=8)

plt.title("Historial de precios y decisiones BTC")
plt.xlabel("Fecha")
plt.ylabel("Precio (MXN)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

