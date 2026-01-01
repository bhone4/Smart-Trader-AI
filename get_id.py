import requests
import time

# ဒီနေရာမှာ BotFather ပေးတဲ့ Token အရှည်ကြီးကို ထည့်ပါ
TOKEN = "8072730581:AAHWgYcKKCxNmCXuuYVhvRufE4SIl49BBGY" 

def get_chat_id():
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    print("Checking for updates...")
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # ရလာတဲ့ Result ကို စစ်မယ်
        if "result" in data and len(data["result"]) > 0:
            # နောက်ဆုံးပို့လိုက်တဲ့ စာကို ယူမယ်
            last_message = data["result"][-1]
            chat_id = last_message["message"]["chat"]["id"]
            first_name = last_message["message"]["chat"]["first_name"]
            
            print("\n✅ တွေ့ပါပြီ!")
            print(f"👤 Name: {first_name}")
            print(f"🆔 YOUR CHAT ID: {chat_id}")
            print("-----------------------------------")
            print("ဒီ Chat ID ကို config.py မှာ သွားထည့်လိုက်ပါ!")
        else:
            print("\n❌ ဘာစာမှ မတွေ့ပါ။")
            print("နည်းလမ်း: Telegram မှာ Bot ကိုဖွင့်ပြီး 'Hello' လို့ စာအရင်ပို့လိုက်ပါ။ ပြီးမှ ပြန် run ပါ။")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_chat_id()
