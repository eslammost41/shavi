
from flask import Flask, request
import requests
from datetime import datetime
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "8040681657:AAE0byVVsLKxt8wFqJrceRCqAwLVPVpea4g")
BOT_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
SHEET_URL = os.getenv("SHEET_URL", "https://your-sheet-webhook.com/save")

def send_message(chat_id, text):
    data = {"chat_id": chat_id, "text": text}
    requests.post(BOT_URL, json=data)

def save_to_sheet(phone):
    data = {
        'timestamp': str(datetime.now()),
        'phone': phone,
        'source': 'Telegram Webhook'
    }
    requests.post(SHEET_URL, json=data)

@app.route('/', methods=["POST"])
def webhook():
    data = request.get_json()
    if 'message' in data:
        message = data['message']
        chat_id = message['chat']['id']
        text = message.get('text', '').lower()
        if 'start' in text or 'أهلاً' in text:
            send_message(chat_id, "أهلاً وسهلاً! إحنا Shavi Agency. ممكن نعرف أكتر عن مشروعك؟")
        elif text.startswith('010') or text.startswith('011'):
            save_to_sheet(text)
            send_message(chat_id, "شكراً ليك، تم تسجيل رقمك وهنكلمك قريب ✅")
        else:
            send_message(chat_id, "ممكن توضح أكتر؟ إحنا معاك خطوة بخطوة.")
    return 'ok'
