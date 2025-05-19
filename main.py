import os
import time
import datetime
import requests
import numpy as np

BOT_TOKEN = os.getenv("7864705902:AAFrCAicFGeTfpXDiKEfMiKqYfwngNFa8Ts")
CHAT_ID = os.getenv("6679590529")
SYMBOL = os.getenv("SYMBOL", "BTCUSDT")
INTERVAL = "1m"
RSI_THRESHOLD = 30

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    try:
        requests.post(url, data=data)
    except:
        pass

def get_prices(symbol):
    url = f"https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": INTERVAL, "limit": 100}
    r = requests.get(url, params=params)
    return [float(x[4]) for x in r.json()]

def calculate_rsi(prices, period=14):
    deltas = np.diff(prices)
    ups = deltas[deltas > 0].sum() / period
    downs = -deltas[deltas < 0].sum() / period
    rs = ups / downs if downs != 0 else 0
    rsi = 100 - (100 / (1 + rs))
    return rsi

while True:
    try:
        prices = get_prices(SYMBOL)
        rsi = calculate_rsi(prices)
        last_price = prices[-1]
        now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        if rsi < RSI_THRESHOLD:
            send_telegram(f"[{now} UTC] RSI = {rsi:.2f} (LOW) | Cena: {last_price}")
        print(f"{now} | RSI: {rsi:.2f} | Cena: {last_price}")
        time.sleep(60)
    except Exception as e:
        send_telegram(f"Błąd: {e}")
        time.sleep(60)
