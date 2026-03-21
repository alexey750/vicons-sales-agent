import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import openai
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Конфиг
BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
LEAD_WEBHOOK = os.getenv('LEAD_WEBHOOK')  # https://script...

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

# Vicons услуги
VICONS_SERVICES = """
💼 *Бухгалтерские услуги Виктория Консалт:*

• **Старт** 6 000₽/мес — ИП, ОСНО
• **Лайт** 9 000₽/мес — УСН  
• **Уверенный** 12 000₽/мес — полный пакет

🎁 *Акция: -15% новым клиентам!*
📞 vicons.ru
"""

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("💼 Услуги", callback_data="services"))
    markup.add(InlineKeyboardButton("💬 Бесплатная консультация", callback_data="consult"))
    markup.add(InlineKeyboardButton("📞 Заказать звонок", callback_data="lead"))
    
    bot.send_message(message.chat.id,
        "👋 *Добро пожаловать в Виктория Консалт!*\n\n"
        "✅ Бухгалтерия для ИП и ООО\n"
        "✅ Регистрация бизнеса\n"
        "✅ Налоговый учёт\n\n"
        f"{VICONS_SERVICES}\n\n"
        "Чем поможем?", 
        parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    cid = call.message.chat.id
    mid = call.message.id
    
    if call.data == "services":
        bot.edit_message_text(f"{VICONS_SERVICES}\n\nВыберите:", 
            cid, mid, parse_mode='Markdown', reply_markup=start_keyboard())
    
    elif call.data == "consult":
        bot.send_message(cid, "💬 *Задайте вопрос бухгалтеру*\n(ИИ GPT-4o анализирует):", parse_mode='Markdown')
        bot.register_next_step_handler(call.message, gpt_consult)
    
    elif call.data == "lead":
        bot.send_message(cid, 
            "📞 *Оставьте заявку!*\n\n"
            "Напишите:\n• Имя\n• Телефон\n• Нужная услуга\n\n"
            "Менеджер перезвонит *за 15 минут!*", 
            parse_mode='Markdown')

def start_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("💬 Консультация", callback_data="consult"))
    markup.add(InlineKeyboardButton("📞 Заказать звонок", callback_data="lead"))
    return markup

def gpt_consult(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": 
                 "Ты эксперт-бухгалтер Виктория Консалт. "
                 "Услуги: Старт(6000₽), Лайт(9000₽), Уверенный(12000₽). "
                 "Акция -15%. Рекомендуй пакеты, собирай лиды."},
                {"role": "user", "content": message.text}
            ],
            max_tokens=300
        )
        bot.reply_to(message, f"🤖 *Бухгалтер:* {response.choices[0].message.content}", parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, "❌ Ошибка GPT. Попробуйте позже.")

@bot.message_handler(func=lambda m: True)
def collect_lead(message):
    data = {
        'Имя': message.from_user.first_name or 'Неизвестно',
        'Телефон': message.text,
        'Email': '',
        'Услуга': 'Консультация Виктория Консалт'
    }
    
    try:
        requests.post(LEAD_WEBHOOK, data=data, timeout=5)
        bot.reply_to(message, 
            "✅ *Заявка принята в CRM!*\n\n"
            "📞 Менеджер *Виктория Консалт* перезвонит\n"
            "в течение *15 минут*\n\n"
            "Спасибо за доверие! 🎯", parse_mode='Markdown')
    except:
        bot.reply_to(message, "❌ Ошибка отправки. Напишите администратору.")

print("🚀 Vicons Sales Bot запущен!")
bot.polling(none_stop=True)
