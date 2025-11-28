# Copilot Instructions for Crypto Trading Monitoring System

## Project Overview
This is a cryptocurrency price monitoring and automated trading system for the Bitso exchange. It tracks BTC, ETH, XRP, LTC, and TUSD prices, sets price alerts, and executes conditional buy/sell orders.

## Architecture & Data Flow

### Core Components

1. **Data Collection (`recolector.py`)**
   - Periodically fetches prices from Bitso API for multiple trading pairs
   - Appends timestamped prices to CSV files (e.g., `bitcoin_precios.csv`)
   - Stores data locally for historical analysis
   - Key pairs: `btc_mxn`, `eth_mxn`, `xrp_mxn`, `ltc_mxn`, `tusd_mxn`

2. **Alert System (`Alerta.py`)**
   - Monitors configured price thresholds (`umbrales` dict)
   - Queries Bitso API for current prices
   - Emits alerts when thresholds are crossed
   - Currently uses hardcoded thresholds (should migrate to config)

3. **API Integration (`Bitso.py`)**
   - Wraps Bitso REST API (v3)
   - Implements request signing with HMAC-SHA256 for authenticated endpoints
   - Provides market price queries (`get_market_price()`)
   - Executes limit orders (`place_order()`) with book, side, amount, price parameters
   - **Requires environment variables:** `API_KEY`, `API_SECRET` (currently hardcoded placeholders)

4. **Trading Logic**
   - `EstableceCompra.py`: Buy orders based on price thresholds
   - `UmbralVentaTUSD.py`: Sell logic for TUSD with cost-based thresholds
   - Both implement threshold-based decision rules with time-based polling

5. **Analysis & Visualization**
   - `Grafica.py`: Plots price history from CSV
   - `GraficaDespy.py`: Overlay decisions on price charts
   - Uses pandas for data loading and matplotlib for plotting

## Critical Patterns & Conventions

### API Communication
- All Bitso requests use `requests.get/post()` with error handling on status codes
- Authenticated requests require `Authorization: Bitso {API_KEY}:{nonce}:{signature}` header
- Nonce is millisecond timestamp: `int(time.time() * 1000)`
- Message format for signing: `nonce + http_method + url_path + params`

### Data Storage
- **CSV-based persistence:** Each asset stores price history locally (timestamp, price)
- **File paths are hardcoded** using absolute Windows paths (e.g., `C:\\Viboron\\BTC_precios.csv`)
- CSV format: `fecha,precio` (datetime string, float)
- This is a significant limitation for cross-platform use

### Trading Decision Logic
- Price thresholds defined in dictionaries (volatile to hardcoding)
- Decisions based on:
  - Static thresholds (fixed price limits)
  - Moving averages (7-day and 30-day windows)
  - Standard deviation bands (mean ± std)
  - Cost-based calculations (fixed + variable costs per unit)

## Developer Workflows

### Testing Price Alert Logic
```python
# Test threshold comparison without API
umbrales = {"btc_mxn": 600000}
precio = 595000
if precio < umbrales["btc_mxn"]:
    print("Would trigger buy alert")
```

### Running Data Collection
- Execute `recolector.py` periodically (cron job or scheduled task)
- Verify CSV files populate in `C:\\Viboron\\` directory
- Check latest price: read last line of CSV

### Debugging API Authentication
- Verify `API_KEY` and `API_SECRET` are set correctly (currently placeholder strings)
- Check nonce generation: should be current milliseconds
- Test signature locally with known request before executing orders

### Adding New Crypto Pairs
1. Add pair to `libros` list in `recolector.py` (e.g., `"doge_mxn"`)
2. Add threshold to `umbrales` dict in `Alerta.py`
3. Create corresponding CSV file or let collector initialize it
4. Update visualization scripts to include new pair

## Important Caveats & Anti-Patterns

### Security Issues
- **API credentials are hardcoded** in `Bitso.py` (lines 5-6) — must use environment variables
- No validation of API responses before casting to float
- No rate limiting on API requests

### Data Pipeline Issues
- **Absolute Windows paths** hardcoded everywhere — breaks on Linux/Mac or different system layouts
- **Manual CSV header management** — files created without headers, parsed with `names=` parameter
- **No data validation** — assumes all API responses have expected structure

### Operational Issues
- Alert thresholds hardcoded in source → requires code change to adjust alerts
- No logging framework — all output uses `print()` statements
- `UmbralVentaTUSD.py` has infinite loop (`while True`) with no shutdown mechanism
- Backup files exist (`.bak` files) but no clear versioning strategy

## Code Style Notes
- File naming uses PascalCase for main modules (`Alerta.py`, `Bitso.py`)
- Docstrings are absent — rely on code clarity and variable names
- Functions use underscores (snake_case): `get_market_price()`, `place_order()`
- Heavy reliance on external APIs with minimal abstraction layer

## Integration Points & Dependencies
- **Bitso API v3:** All price queries and order placement
- **Python packages:** `requests`, `pandas`, `matplotlib`
- **OS filesystem:** Local CSV storage requires write permissions to `C:\\Viboron\\`
- **System time:** Used for nonce generation in API signatures

## Recommended Next Steps for Enhancement
1. Externalize configuration (thresholds, file paths, API credentials)
2. Add proper logging with timestamp and log levels
3. Implement request retries and rate limiting
4. Add unit tests for decision logic (threshold comparisons)
5. Consider database instead of CSV for performance
6. Add monitoring/alerting for failed API requests
