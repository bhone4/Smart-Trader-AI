import pandas as pd
from binance.spot import Spot

def get_market_data():
    try:
        # Binance Client ကို ဖန်တီးမယ်
        client = Spot()
        
        # Data ဆွဲမယ် (BTCUSDT)
        # 15m (၁၅ မိနစ်), limit=100
        klines = client.klines("BTCUSDT", "15m", limit=100)
        
        # ရလာတဲ့ Data ကို ဇယားဖွဲ့မယ်
        # Binance data structure: [Time, Open, High, Low, Close, Volume, ...]
        df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'q_vol', 'num_trades', 't_base', 't_quote', 'ignore'])
        
        # မလိုတာတွေ ဖျက်မယ်
        df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
        
        # Data type တွေကို ဂဏန်းအဖြစ် ပြောင်းမယ် (သူက String နဲ့ လာတတ်လို့)
        df = df.astype(float)
        
        # အချိန်ပုံစံ ပြောင်းမယ်
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        return df
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

