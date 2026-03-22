import os
from flask import Flask
import telebot
from openai import OpenAI
from threading import Thread

# Токены
TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=OPENAI_API_KEY)
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/health')
def health():
    return 'OK - Vicons Bot жив!'

@bot.message_handler(commands=['start', '/start'])
def start(message):
    welcome = """👋 *Виктория Консалт* — бухгалтерские и юридические услуги!

*📍 Адрес:* ул. Маршала Тухачевского д.22 оф. 412
*📧 Почта:* info@vicons.ru  
*📞 Телефон:* 8 (812) 207 13-76
*🌐 Сайт:* www.vicons.ru

*Помогу с:*
• юридические услуги
• бухгалтерия
• регистрация бизнеса

Напиши задачу! 💼"""
    bot.reply_to(message, welcome, parse_mode='Markdown', disable_web_page_preview=True)

@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"""Ты онлайн-агент *Виктория Консалт* (www.vicons.ru).

*Контакты фирмы (ВСЕГДА указывай):*
- Адрес: ул. Маршала Тухачевского д.22 оф. 412  
- Телефон: 8 (812) 207 13-76
- Email: info@vicons.ru
- Сайт: www.vicons.ru

*Роль:* Профессиональный консультант и продавец бухгалтерских и юридических услуг.  
Убеждай мягко, предлагай решения, закрывай на звонок/письмо.

Отвечай как менеджер: 'Помогу с...', 'Звонок?', 'Письмо?'"""
                },
                {"role": "user", "content": message.text}
            ],
            max_tokens=600
        )
        bot.reply_to(message, response.choices[0].message.content, parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка. Звони: 8 (812) 207 13-76 | info@vicons.ru")

def run_bot():
    print("🤖 Vicons Bot START")
    bot.polling(none_stop=True)

if __name__ == '__main__':
    bot_thread = Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    port = int(os.environ.get('PORT', 10000))
    print(f"🌐 Healthcheck PORT {port}")
    app.run(host='0.0.0.0', port=port)
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
    welcome_text = """👋 *Привет! Я онлайн-агент компании Виктория Консалт* (vicons.ru)

*Что мы делаем:*
• юридические услуги
• бухгалтерия
• регистрация бизнеса

*Напиши что нужно* — подберу решение + коммерческое предложение!

📞 8 (812) 207 13-76
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
                    "content": """Ты *онлайн-агент компании Виктория Консалт* (vicons.ru). 

*Твоя роль:*
- Всегда представляйся: "онлайн-агент Виктория Консалт"
- Консультируешь по: юридические услуги, бухгалтерия, регистрация бизнеса
- Быть убедительным продавцом 
- Предлагать услуги + контакты
- Заканчивать призывом к действию

*Контакты:* 8 (812) 207 13-76, info@vicons.ru

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
        bot.reply_to(message, f"🤖 Извини, техническая ошибка. Напиши /start или звони 8 (812) 207 13-76")

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
import requests

def send_to_sheets(name, phone, email, message, chat_id):
    WEBHOOK_URL = 'https://script.google.com/macros/s/AKfycbzeVABvlKDhWx2PBwsxV91sJu2qFaA74mDNotga-tFbE4sZao2yzaiyo5_GCivqW752/exec'  # из шага 3
    
    data = {
        'chatId': chat_id,
        'name': name,
        'phone': phone,
        'email': email,
        'message': message
    }
    
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        print(f"✅ Лид сохранён: {response.json()}")
    except Exception as e:
        print(f"❌ Ошибка Sheets: {e}")

# Вызывай в обработчиках лидов:
# send_to_sheets(user_name, user_phone, user_email, user_msg, message.chat.id)
