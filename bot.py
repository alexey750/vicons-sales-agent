import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from openai import OpenAI
import requests

print("1. Vicons Bot DEBUG START")

# Загрузка переменных ОКРУЖЕНИЯ
BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENAI_API_KEY
