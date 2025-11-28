import os
import requests, time, hmac, hashlib, json
from datetime import datetime

# Credentials are read from environment variables for safety.
# Set `API_KEY` and `API_SECRET` in the environment before running code that places orders.
API_KEY = os.environ.get('API_KEY', 'TU_API_KEY')
API_SECRET = os.environ.get('API_SECRET', 'TU_API_SECRET').encode()
BASE_URL = 'https://api.bitso.com'


def get_market_price(book='btc_mxn'):
    url = f'{BASE_URL}/v3/ticker/?book={book}'
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Bitso ticker request failed: {res.status_code} {res.text}')
    payload = res.json().get('payload')
    if not payload or 'last' not in payload:
        raise RuntimeError('Unexpected Bitso ticker response structure')
    return float(payload['last'])


def sign_request(http_method, url_path, nonce, params=''):
    message = nonce + http_method + url_path + params
    signature = hmac.new(API_SECRET, message.encode(), hashlib.sha256).hexdigest()
    return signature


def place_order(book, side, amount, price):
    url_path = '/v3/orders/'
    nonce = str(int(time.time() * 1000))
    payload = json.dumps({
        'book': book,
        'side': side,
        'type': 'limit',
        'major': str(amount),
        'price': str(price)
    })
    signature = sign_request('POST', url_path, nonce, payload)
    headers = {
        'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}',
        'Content-Type': 'application/json'
    }
    res = requests.post(BASE_URL + url_path, headers=headers, data=payload)
    if res.status_code not in (200, 201):
        raise RuntimeError(f'Order placement failed: {res.status_code} {res.text}')
    return res.json()


if __name__ == '__main__':
    # Example: Compra 0.001 BTC si el precio está por debajo de $600,000 MXN
    try:
        price = get_market_price()
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("fecha actual:", fecha)
        print("Precio actual btc_mxn:", price)

        if price < 600000:
            resp = place_order('btc_mxn', 'buy', 0.001, price)
            print("¡Orden enviada!", resp)
        else:
            print("Precio demasiado alto. No se realizó compra.")
    except Exception as e:
        print("Error during example run:", e)