import os
import pandas as pd
import matplotlib.pyplot as plt
from config import data_path


def main():
    csv_file = data_path("btc_decisiones.csv")
    if not os.path.exists(csv_file):
        print(f"Data file not found: {csv_file}. Generate decision CSV first.")
        return

    df = pd.read_csv(csv_file, names=["Fecha", "Precio", "Decision"])
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


if __name__ == '__main__':
    main()

