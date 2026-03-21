import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from openai import OpenAI
import requests
import traceback

# Debug
print("🚀 1. Vicons Bot starting...")
print(f"🚀 2. BOT_TOKEN: {'OK' if os.getenv('BOT_TOKEN') else 'MISSING'}")
print(f"🚀 3. OPENAI_KEY: {'OK' if os.getenv('OPENAI_API_KEY') else 'MISSING'}")
print(f"🚀 4. LEAD_WEBHOOK: {'OK' if os.getenv('LEAD_WEBHOOK') else 'MISSING'}")

# Env
BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
LEAD_WEBHOOK = os.getenv('LEAD_WEBHOOK')

if not BOT_TOKEN:
    print("❌ ERROR: BOT_TOKEN missing!")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

# OpenAI
try:
    client = OpenAI(api_key=OPENAI_API_KEY)
    print("🚀 5. OpenAI client OK")
except:
    print("⚠️ OpenAI key problem, continuing...")
    client = None

# Vicons данные
SERVICES = """
💼 *Виктория Консалт — бухгалтерия для бизнеса*

📋 **Пакеты услуг:**
• *Старт* — 6 000₽/мес (ИП, ОСНО)
• *Лайт* — 9 000₽/мес (УСН 6%)
• *Уверенный* — 12 000₽/мес (полный пакет)

🎁 **Акция: -15% новым клиентам!**
🌐 vicons.ru
"""

@bot.message_handler(commands=['start'])
def start(message):
    print(f"👤 /start from {message.from_user.username}")
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("💼 Посмотреть услуги", callback_data="services"))
    markup.add(InlineKeyboardButton("💬 Бесплатная консультация GPT", callback_data="gpt"))
    markup.add(InlineKeyboardButton("📞 Заказать звонок менеджера", callback_data="lead"))
    
    bot.send_message(message.chat.id,
        "👋 *Добро пожаловать в Виктория Консалт!*\n\n"
        "✅ Бухгалтерское сопровождение ИП и ООО\n"
        "✅ Налоговый учёт и отчётность\n"
        f"{SERVICES}\n\n"
        "Чем поможем сегодня?", 
        parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    cid = call.message.chat.id
    
    if call.data
