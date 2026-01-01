import time
import requests
from datetime import datetime
from data_loader import get_market_data
from indicators import add_indicators # နာမည်ပြောင်းထားတယ်နော်
import config

def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": config.TELEGRAM_CHAT_ID, "text": message}
        requests.post(url, data=data)
    except Exception as e:
        print(f"❌ Telegram Error: {e}")

def run_bot():
    print(f"🤖 Smart AI Bot (RSI + MACD) စတင် run နေပါပြီ...\n")
    
    while True:
        try:
            print(f"⏳ {datetime.now().strftime('%H:%M:%S')} - ဈေးကွက်ကို စစ်ဆေးနေသည်...")
            
            df = get_market_data()
            
            if df is not None:
                # တွက်ချက်မှုများ ပြုလုပ်ခြင်း
                df = add_indicators(df)
                latest = df.iloc[-1]
                
                # Data များကို ဆွဲထုတ်ခြင်း
                price = latest['close']
                rsi = latest['rsi']
                macd = latest['macd']
                signal = latest['macd_signal']
                
                # Trend ကို သတ်မှတ်ခြင်း
                trend = "UP 🟢" if macd > signal else "DOWN 🔴"
                
                print(f"💰 Price: ${price:,.2f}")
                print(f"📊 RSI: {rsi:.2f}")
                print(f"📈 Trend: {trend}")
                print("-" * 30)
                
                # --- ဆုံးဖြတ်ချက်ချမည့် အပိုင်း (Logic) ---
                message = ""
                
                # 1. ဝယ်မည့် အခြေအနေ (RSI နည်းပြီး Trend တက်နေရင် ပိုသေချာတယ်)
                if rsi < 35 and macd > signal:
                    print("🚀 STRONG BUY SIGNAL! (RSI Cheap + Trend Up)")
                    message = f"🚀 **STRONG BUY ALERT** 🚀\n\nCoin: {config.SYMBOL}\nPrice: ${price:,.2f}\nRSI: {rsi:.2f} (Cheap)\nTrend: UP 🟢\n\nအခြေအနေကောင်းနေပါပြီ၊ ဝယ်ဖို့စဉ်းစားပါ။"
                    send_telegram_message(message)
                
                # 2. ရောင်းမည့် အခြေအနေ
                elif rsi > 70:
                    print("⚠️ SELL SIGNAL! (Overbought)")
                    message = f"⚠️ **SELL ALERT** ⚠️\n\nCoin: {config.SYMBOL}\nPrice: ${price:,.2f}\nRSI: {rsi:.2f}\nTrend: {trend}\n\nဈေးအရမ်းတက်နေပါပြီ၊ ရောင်းဖို့စဉ်းစားပါ။"
                    send_telegram_message(message)
                    
            # ၁ မိနစ် နားမည်
            time.sleep(60)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    run_bot()


