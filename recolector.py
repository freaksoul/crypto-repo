import requests, csv, os
from datetime import datetime
from config import data_path

# Lista de libros disponibles en Bitso
libros = ["btc_mxn", "eth_mxn", "xrp_mxn", "ltc_mxn"]

def guardar_precios():
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for libro in libros:
        url = f"https://api.bitso.com/v3/ticker/?book={libro}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            precio = data['payload']['last']
            nombre = libro.split("_")[0].upper()

            target = data_path(f"{nombre}_precios.csv")
            # Ensure directory exists (data_path already does this) but keep safe
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, mode="a", newline="", encoding="utf-8") as archivo:
                writer = csv.writer(archivo)
                writer.writerow([fecha, precio])

            print(f"✅ {nombre}: {fecha} - ${precio} MXN (saved to {target})")
        else:
            print(f"❌ Error con {libro}: {response.status_code}")

