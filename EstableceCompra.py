import argparse
import os
import pandas as pd
from config import data_path


def compute_stats(csv_file: str):
	df = pd.read_csv(csv_file, names=["fecha", "precio"], parse_dates=["fecha"])
	if df.empty:
		raise ValueError("CSV is empty")
	df.sort_values("fecha", inplace=True)

	precio_promedio = df["precio"].tail(7).mean()
	precio_minimo = df["precio"].tail(30).min()
	std = df["precio"].tail(30).std()
	media = df["precio"].tail(30).mean()
	umbral_compra = media - std

	return precio_promedio, precio_minimo, umbral_compra


def main():
	parser = argparse.ArgumentParser(description="Calcular estadísticas de compra sugerida a partir de CSV de precios.")
	parser.add_argument("--file", "-f", default="BTC_precios.csv", help="CSV filename under the data directory (default: BTC_precios.csv)")
	args = parser.parse_args()

	csv_file = data_path(args.file)
	if not os.path.exists(csv_file):
		print(f"Data file not found: {csv_file}. Run `recolector.py` first.")
		return

	try:
		precio_promedio, precio_minimo, umbral_compra = compute_stats(csv_file)
	except Exception as e:
		print(f"Error reading or processing CSV {csv_file}: {e}")
		return

	print(f"📊 Precio promedio últimos 7 días: ${precio_promedio:,.0f} MXN (from {csv_file})")
	print(f"📉 Precio mínimo últimos 30 días: ${precio_minimo:,.0f} MXN")
	print(f"🎯 Umbral de compra sugerido: ${umbral_compra:,.0f} MXN")


if __name__ == '__main__':
	main()

