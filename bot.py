import requests
import time
from groq import Groq

TELEGRAM_TOKEN = "8904774489:AAH7ethN1bWR8KApZ-MBBuOwkhz3n7Wejss"
GROQ_API_KEY = "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"
CHAT_ID = ""

client = Groq(api_key=GROQ_API_KEY)

def get_price(symbol):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}=X"
        r = requests.get(url, timeout=10)
        data = r.json()
        price = data['chart']['result'][0]['meta']['regularMarketPrice']
        return price
    except:
        return None

def analyze_market(symbol, price):
    prompt = f"""انت محلل تداول خبير. السعر الحالي لـ {symbol} هو {price}.
حلل السوق وقرر:
1. هل تشتري ام تبيع ام تنتظر؟
2. سعر الدخول المناسب
3. Stop Loss المناسب
4. Take Profit المناسب
5. نسبة ثقتك في القرار
اجب بشكل مختصر وواضح."""
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    re
