import os
from flask import Flask
import telebot
from openai import OpenAI
from threading import Thread

TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/health')
def health():
    return 'OK'

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Vicons Sales Agent готов! 🚀")

@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": message.text}]
        )
        bot.reply_to(message, response.choices[0].message.content)
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {str(e)}")

def run_bot():
    print("🤖 Vicons Bot START")
    bot.polling(none_stop=True)

if __name__ == '__main__':
    bot_thread = Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    port = int(os.environ.get('PORT', 10000))
    print(f"🌐 Healthcheck на PORT {port}")
    app.run(host='0.0.0.0', port=port)
