import telegram
import telebot
import time
import psycopg2
import shutil
from telegram import Bot
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telebot import types

bot = telebot.TeleBot('6200718668:AAHgKDoey-TcqdvIK-dgDNpdWKCXHDoaEqQ')

DB_HOST = 'localhost'
DB_NAME = 'demo'
DB_USER = 'postgres'
DB_PASSWORD = 'qwerty'

main = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("Начать проверку статуса")
btn2 = types.KeyboardButton("Резервное копирование")
btn3 = types.KeyboardButton("Восстановление")
main.add(btn1, btn2, btn3)

def check_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

        return "Подключение к PostgreSQL успешно!"
    except Exception as e:
        return f"Ошибка подключения к PostgreSQL: {str(e)}"

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я тестовый бот для проверки базы данных".format(message.from_user), reply_markup=main)
    while True:
        bot.send_message(message.chat.id, check_db_connection())
        time.sleep(15)

@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == "Начать проверку статуса"):
        bot.send_message(message.chat.id, check_db_connection())
    elif (message.text == "Резервное копирование"):
        bot.send_message(message.chat.id, text="Копия успешно создана")

    elif (message.text == "Восстановление"):
        bot.send_message(message.chat.id, text="Восстоновление с помощью резервной копии была успешна", reply_markup=main)
        shutil.copyfile('copytext.txt','text.txt')
    else:
        bot.send_message(message.chat.id, text="Не понимать")
bot.polling()