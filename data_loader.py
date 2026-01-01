import ccxt
import pandas as pd
import config

def get_market_data():
    try:
        # Binance ကို ချိတ်တဲ့အခါ options ထည့်ပေးလိုက်မယ်
        exchange = ccxt.binance({
            'enableRateLimit': True, # အမြန်နှုန်း ထိန်းညှိခြင်း
            'options': {
                'defaultType': 'spot' # <--- ဒီနေရာမှာ Spot ကို အသေမှတ်ပေးလိုက်တာ
            }
        })
        
        # Data ဆွဲမယ်
        ohlcv = exchange.fetch_ohlcv(config.SYMBOL, timeframe=config.TIMEFRAME, limit=config.LIMIT)
        
        # DataFrame ပြောင်းမယ်
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        return df
    except Exception as e:
        # Error အကြောင်းရင်းကို ရှင်းရှင်းလင်းလင်း ပြခိုင်းမယ်
        print(f"Error fetching data: {e}") 
        return None
