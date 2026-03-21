import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import openai
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os
import json

load_dotenv()

# Токены
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
openai.api_key = os.getenv('OPENAI_API_KEY')
SHEET_ID = os.getenv('GOOGLE_SHEETS_ID')

# Vicons данные
VICONS_SERVICES = """
Бухгалтерское сопровождение:
- Старт: 6000₽/мес (ИП, ОСНО)
- Лайт: 9000₽/мес (УСН)
- Уверенный: 12000₽/мес (полный пакет)
Акция: -15% новым клиентам!
"""

# Google Sheets
gc = gspread.service_account(filename='credentials.json')  # TODO: настрой сервисный аккаунт
sheet = gc.open_by_key(SHEET_ID).sheet1

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("💼 Услуги", callback_data="services"))
    markup.add(InlineKeyboardButton("💬 Консультация", callback_data="consult"))
    markup.add(InlineKeyboardButton("📞 Заказать звонок", callback_data="lead"))
    bot.send_message(message.chat.id, 
        "👋 Добро пожаловать в *Виктория Консалт*!\n\n"
        "Мы ведём бухгалтерию для ИП и ООО.\n"
        f"{VICONS_SERVICES}\n\n"
        "Чем поможем?", 
        parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "services":
        bot.edit_message_text(
            f"💼 *Наши услуги:*\n\n{VICONS_SERVICES}\n\n"
            "Нужна консультация?", 
            call.message.chat.id, call.message.id, parse_mode='Markdown')
    
    elif call.data == "consult":
        bot.edit_message_text(
            "💬 Задайте вопрос бухгалтеру (GPT-4o):", 
            call.message.chat.id, call.message.id)
        bot.register_next_step_handler(call.message, consult_gpt)
    
    elif call.data == "lead":
        bot.edit_message_text(
            "📞 Оставьте контакты — перезвоним за 15 мин!\n\n"
            "Имя, телефон, услуга:", 
            call.message.chat.id, call.message.id)
        bot.register_next_step_handler(call.message, collect_lead)

def consult_gpt(message):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты бухгалтер Виктория Консалт. Рекомендуй услуги: Старт(6000₽), Лайт(9000₽), Уверенный(12000₽). Акция -15%."},
            {"role": "user", "content": message.text}
        ]
    )
    bot.reply_to(message, response.choices[0].message.content)

def collect_lead(message):
    data = {
        'Имя': message.from_user.first_name,
        'Телефон': 'не указан',
        'Email': 'не указан',
        'Услуга': message.text,
        'Дата': '2026-03-21'
    }
    sheet.append_row(list(data.values()))
    bot.reply_to(message, 
        "✅ Заявка принята!\n"
        "Менеджер перезвонит в течение 15 минут.\n"
        f"Спасибо, {message.from_user.first_name}!")

bot.polling()
