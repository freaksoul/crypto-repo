# CryptoProyecto — Bitso price monitoring and simple trading helpers

Brief repo for collecting prices from Bitso, evaluating simple thresholds,
and (optionally) placing limit orders. The code uses CSV files for local
storage and small plotting utilities for visualization.

**Important:** this project uses absolute Windows paths by default but has
been updated to support a configurable data directory via the
`VIBORON_DATA_DIR` environment variable (see below).

**Quick start**

1. Create a Python virtualenv and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. (Optional) Set a custom data directory and API credentials in PowerShell:

```powershell
$env:VIBORON_DATA_DIR = 'D:\mydata\crypto'
$env:API_KEY = 'your_api_key'
$env:API_SECRET = 'your_api_secret'
```

3. Collect prices (appends CSVs to the data dir):

```powershell
python recolector.py
```

4. Run analysis or plotting utilities, e.g.:

```powershell
python EstableceCompra.py
python Grafica.py
python GraficaDespy.py
python MonitorBTC.py
```

Files of interest
- `recolector.py` — fetches tickers and appends to CSVs (uses `config.data_path()`)
- `Bitso.py` — Bitso API helpers and order placement (reads `API_KEY`/`API_SECRET` from env)
- `Alerta.py` — threshold-based alerts (prints to console)
- `EstableceCompra.py`, `MonitorBTC.py` — decision logic and simple logging
- `Grafica.py`, `GraficaDespy.py` — plotting utilities

CSV format and location
- Default base data dir: `C:\Viboron` (use `VIBORON_DATA_DIR` to override)
- CSV files are stored under the base dir, filenames like `BTC_precios.csv`,
	`BTC_decisiones.csv`, etc.
- CSV rows: `fecha,precio` or `fecha,precio,decision` depending on file. New code
	reads CSVs with explicit column names to avoid header assumptions.

Security & operational notes
- Do not commit real API keys. Store them in environment variables as shown above.
- `Bitso.place_order()` will raise an exception on non-2xx responses; only run
	order-placement code when you intend to trade.
- Many scripts use `print()` for logging; consider adding a logging framework
	for production usage.

If you'd like, I can:
- Add a short CONTRIBUTING or developer README section with recommended workflows.
- Create a `dev-requirements.txt` with linting/test tools.
"# crypto-repo" 
