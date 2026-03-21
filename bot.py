import os
import telebot
from openai import OpenAI

TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # ← ЭТО!

client = OpenAI(api_key=OPENAI_API_KEY)
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Vicons Sales Agent готов! 🚀")

@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": message.text}]
    )
    bot.reply_to(message, response.choices[0].message.content)

print("1. Vicons Bot DEBUG START")
from flask import Flask
app = Flask(__name__)

@app.route('/health')
def health():
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

bot.polling(none_stop=True)
