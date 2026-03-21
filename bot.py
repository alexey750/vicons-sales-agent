import os
from flask import Flask
import telebot
from openai import OpenAI
from threading import Thread

# Токены из Render Environment
TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Инициализация
client = OpenAI(api_key=OPENAI_API_KEY)
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/health')
def health():
    return 'OK - Vicons Bot жив!'

@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = """👋 *Привет! Я Sales Agent компании Виктория Консалт* (vicons.ru)

*Что мы делаем:*
• Веб-разработка и сайты любой сложности
• CRM системы под ключ
• IT-консультации для бизнеса
• Digital-маркетинг

*Напиши что нужно* — подберу решение + коммерческое предложение!

📞 +7 (495) 777-77-77
✉️ info@vicons.ru"""
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": """Ты *Sales Agent компании Виктория Консалт* (vicons.ru). 

*Твоя роль:*
- Всегда представляйся: "Sales Agent Виктория Консалт"
- Консультируешь по IT: сайты, CRM, разработка, маркетинг
- Быть убедительным продавцом 
- Предлагать услуги + контакты
- Заканчивать призывом к действию

*Контакты:* +7 (495) 777-77-77, info@vicons.ru

Отвечай профессионально, как менеджер по продажам!"""
                },
                {
                    "role": "user", 
                    "content": f"Клиент: {message.text}"
                }
            ],
            max_tokens=500
        )
        answer = response.choices[0].message.content
        bot.reply_to(message, answer, parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, f"🤖 Извини, техническая ошибка. Напиши /start или звони +7 (495) 777-77-77")

def run_bot():
    print("🤖 Vicons Bot START - Виктория Консалт онлайн!")
    bot.polling(none_stop=True)

if __name__ == '__main__':
    # Бот в фоне
    bot_thread = Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Flask для Render
    port = int(os.environ.get('PORT', 10000))
    print(f"🌐 Healthcheck на PORT {port}")
    app.run(host='0.0.0.0', port=port)
