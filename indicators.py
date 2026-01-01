import pandas as pd

def add_indicators(df):
    """RSI နှင့် MACD နှစ်ခုလုံးကို တွက်ချက်ပေးမည့် Function"""
    
    # --- 1. RSI တွက်ချက်ခြင်း (ဈေးပေါ/ဈေးကြီး ကြည့်ရန်) ---
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))

    # --- 2. MACD တွက်ချက်ခြင်း (ဈေးဦးလှည့်မှု ကြည့်ရန်) ---
    # EMA 12 (ရက်တို) နှင့် EMA 26 (ရက်ရှည်) ကို တွက်သည်
    ema12 = df['close'].ewm(span=12, adjust=False).mean()
    ema26 = df['close'].ewm(span=26, adjust=False).mean()
    
    # MACD Line နှင့် Signal Line ကို ထုတ်သည်
    df['macd'] = ema12 - ema26
    df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
    
    return df

