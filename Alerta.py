import requests
from datetime import datetime

# Umbrales personalizados
umbrales = {
    "btc_mxn": 1300000,
    "eth_mxn": 70000,
    "xrp_mxn": 20
}

def verificar_alertas():
    for libro, umbral in umbrales.items():
        url = f"https://api.bitso.com/v3/ticker/?book={libro}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            precio = float(data['payload']['last'])
            nombre = libro.split("_")[0].upper()

            if precio > umbral:
                print(f"🚨 ALERTA: {nombre} superó ${umbral} MXN → Precio actual: ${precio}")
            else:
                print(f"✅ {nombre} está bajo el umbral → ${precio}")
        else:
            print(f"❌ Error con {libro}: {response.status_code}")

# Ejecutar la verificación
verificar_alertas()