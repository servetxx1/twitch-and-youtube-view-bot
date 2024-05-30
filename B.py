import ccxt
import pandas as pd
import pandas_ta as ta
import logging
from datetime import datetime
import time

# Günlüğü yapılandırma
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Binance API anahtarını ortam değişkenlerinden yükleyin
API_KEY = "U1EC5oue7fomChCGNqWmw16ClERyQj5FIP287mM6CEWDp3NQuikVZZsaPyd7aMqr"
API_SECRET = "uzI3uTgsred3vOH4R702odWwpAszHNiBP90m51imt3qYkVkPyhQhCxp6QQjGobWa"

# Binance'e bağlan
exchange = ccxt.binance({
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'enableRateLimit': True,
})

def calculate_rsi(closes, window=14):
    df = pd.DataFrame(closes, columns=['close'])
    if len(df) < window:
        return None
    rsi = df.ta.rsi(length=window)
    return rsi.iloc[-1] if not rsi.empty else None

def get_balance(symbol):
    try:
        balance = exchange.fetch_balance()
        coin = symbol.split('/')[0]
        coin_balance = balance['total'].get(coin, 0)
        usdt_balance = balance['total'].get('USDT', 0)
        logging.info(f"Mevcut {coin} bakiyesi: {coin_balance}")
        logging.info(f"Mevcut USDT bakiyesi: {usdt_balance}")
        return coin_balance, usdt_balance
    except Exception as e:
        logging.error(f"Bakiye alınırken hata oluştu: {e}")
        return 0, 0

def place_buy_order(symbol, amount_usdt):
    try:
        last_price = exchange.fetch_ticker(symbol)['last']
        amount_coin = amount_usdt / last_price
        order = exchange.create_market_buy_order(symbol, amount_coin)
        logging.info(f"Alım emri verildi: {amount_usdt} USDT karşılığında {amount_coin} {symbol.split('/')[0]} alındı")
    except Exception as e:
        logging.error(f"Alım emri verirken hata oluştu: {e}")

def place_sell_order(symbol, amount_coin):
    try:
        order = exchange.create_market_sell_order(symbol, amount_coin)
        logging.info(f"Satım emri verildi: {amount_coin} {symbol.split('/')[0]} satıldı")
    except Exception as e:
        logging.error(f"Satım emri verirken hata oluştu: {e}")

def fetch_ohlcv(symbol, timeframe='15m', limit=100):
    try:
        data = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        logging.info(f"{len(data)} mum verisi alındı")
        return data
    except Exception as e:
        logging.error(f"OHLCV verisi alınırken hata oluştu: {e}")
        return []

def main(symbol):
    while True:
        coin_balance, usdt_balance = get_balance(symbol)
        
        ohlcv = fetch_ohlcv(symbol, timeframe='15m', limit=100)
        closes = [x[4] for x in ohlcv]

        if not closes:
            logging.warning("Veri alınamadı, 60 saniye sonra tekrar deneniyor...")
            time.sleep(60)
            continue

        rsi_15m = calculate_rsi(closes)
        if rsi_15m is None:
            logging.warning("RSI hesaplanamadı, 60 saniye sonra tekrar deneniyor...")
            time.sleep(60)
            continue

        logging.info(f"15 dakikalık RSI değeri: {rsi_15m}")

        # Alım veya satım sinyallerine göre işlem yapılabilir
        if rsi_15m < 26:  # Alım sinyali
            if usdt_balance > 0.25 * usdt_balance:  # İlk alım
                amount_usdt = usdt_balance * 0.25  # USDT miktarı belirle
                place_buy_order(symbol, amount_usdt)
            elif usdt_balance > 0.33 * usdt_balance:  # İkinci alım
                amount_usdt = usdt_balance * 0.33  # USDT miktarı belirle
                place_buy_order(symbol, amount_usdt)
            elif usdt_balance > 0.5 * usdt_balance:  # Üçüncü alım
                amount_usdt = usdt_balance * 0.5  # USDT miktarı belirle
                place_buy_order(symbol, amount_usdt)
            else:  # Son alım
                amount_usdt = usdt_balance  # USDT miktarı belirle
                place_buy_order(symbol, amount_usdt)

        elif rsi_15m > 70:  # Satım sinyali
            if coin_balance > 0.25 * coin_balance:  # İlk satım
                amount_coin = coin_balance * 0.25  # Coin miktarı belirle
                place_sell_order(symbol, amount_coin)
            elif coin_balance > 0.33 * coin_balance:  # İkinci satım
                amount_coin = coin_balance * 0.33  # Coin miktarı belirle
                place_sell_order(symbol, amount_coin)
            elif coin_balance > 0.5 * coin_balance:  # Üçüncü satım
                amount_coin = coin_balance * 0.5  # Coin miktarı belirle
                place_sell_order(symbol, amount_coin)
            else:  # Son satım
                amount_coin = coin_balance  # Coin miktarı belirle
                place_sell_order(symbol, amount_coin)

        time.sleep(600)  # 15 dakika bekleyin

if __name__ == "__main__":
    symbol = 'SSV/USDT'
    main(symbol)
  
