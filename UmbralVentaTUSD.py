import requests
import time

# Parámetros personalizados
costos_fijos = 0            # en MXN
costo_variable = 18.336          # costo por unidad de TUSD en MXN
cantidad_tusd = 1022            # cantidad que planeas vender

# Calcular umbral de venta por unidad
def calcular_umbral_unitario():
    return costos_fijos / cantidad_tusd + costo_variable

# Obtener precio actual de TUSD/MXN desde Bitso
def obtener_precio_tusd():
    url = "https://api.bitso.com/v3/ticker/?book=tusd_mxn"
    response = requests.get(url)
    data = response.json()
    return float(data['payload']['last'])

# Verificar si es buen momento para vender
def evaluar_venta():
    precio_actual = obtener_precio_tusd()
    umbral = calcular_umbral_unitario()
    print(f"Precio actual: ${precio_actual:.2f} MXN | Umbral: ${umbral:.2f} MXN")
    if precio_actual >= umbral:
        print("✅ Es buen momento para vender TUSD.")
    else:
        print("⏳ Aún no conviene vender TUSD.")

# Ejecutar cada cierto tiempo
while True:
    evaluar_venta()
    time.sleep(3600)  # Espera 1 hora antes de volver a verificar