import os
import requests
import time
from groq import Groq

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    params = {"timeout": 30}
    if offset:
        params["offset"] = offset
    r = requests.get(url, params=params)
    return r.json()

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

def analyze(symbol, price):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": f"انت محلل تداول. السعر الحالي لـ {symbol} هو {price}. قرر: شراء ام بيع ام انتظار؟"}]
    )
    return response.choices[0].message.content

def get_price(symbol):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}=X"
        r = requests.get(url, timeout=10)
        return r.json()['chart']['result'][0]['meta']['regularMarketPrice']
    except:
        return None

print("البوت يعمل")
offset = None
while True:
    updates = get_updates(offset)
    for update in updates.get("result", []):
        offset = update["update_id"] + 1
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")
        if "/start" in text or "/analyze" in text:
            send_message(chat_id, "جاري التحليل...")
            for symbol in ["EURUSD", "XAUUSD", "BTCUSD"]:
                price = get_price(symbol)
                if price:
                    send_message(chat_id, f"📊 {symbol}\n💰 {price}\n\n{analyze(symbol, price)}")
                    time.sleep(5)
    time.sleep(1)
