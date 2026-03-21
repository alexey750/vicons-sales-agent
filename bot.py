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
bot.polling(none_stop=True)
