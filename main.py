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

db_params = {
    'dbname': 'demo',
    'user': 'postgres',
    'password': 'qwerty',
    'host': 'localhost',
}

main = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("Резервное копирование")
btn2 = types.KeyboardButton("Восстановление")
main.add(btn1, btn2)

@bot.message_handler(commands=['start'])
def start(message):
    while True:
        try:
            conn = psycopg2.connect(**db_params)
            cur = conn.cursor()
            # продолжительности самой долгой транзакции
            cur.execute("SELECT max(now() - xact_start) FROM pg_stat_activity;")
            longest_transaction_duration = cur.fetchone()[0]

            # количества активных сессий
            cur.execute("SELECT count(*) FROM pg_stat_activity;")
            active_sessions_count = cur.fetchone()[0]

            # количества сессий со значением lwlock в колонке wait_event
            cur.execute("SELECT count(*) FROM pg_stat_activity WHERE wait_event = 'lwlock';")
            lwlock_sessions_count = cur.fetchone()[0]

            # количество строк в таблице
            cur.execute("SELECT COUNT(*) FROM pg_cast")
            count = cur.fetchone()[0]

            cur.execute("SELECT schema_name FROM information_schema.schemata")
            schemas = cur.fetchall()

            cur.execute("SELECT * FROM pg_stat_activity")
            result = cur.fetchall()
            print(result)


            bot.send_message(message.chat.id, "-----База данных Postgresql успешно подключенна-----")
            bot.send_message(message.chat.id, "Имена табличных пространств: ")
            for schema in schemas:
                bot.send_message(message.chat.id, f"{schema[0]}")

            bot.send_message(message.chat.id, f"\nТекущая активность:\n \n"
                                              f"Количество столбцов в таблице pg_aggregate: {count}\n \n"
                                              f"Продолжительность самой долгой транзакции: {longest_transaction_duration}\n \n"
                                              f"Количество активных сессий: {active_sessions_count}\n \n"
                                              f"Количество сессий со значением lwlock в колонке wait_event: {lwlock_sessions_count}\n \n", reply_markup=main)
            bot.send_message(message.chat.id, "-----------------------------------------------------------------------------------------------")
            cur.close()
            conn.close()

        except psycopg2.Error as e:
            bot.send_message(message.chat.id,f"Ошибка при выполнении SQL-запроса: {e}")
        time.sleep(15)

@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == "Начать проверку статуса"):
        bot.send_message(message.chat.id, "хзхз")
    elif (message.text == "Резервное копирование"):
        bot.send_message(message.chat.id, text="Копия успешно создана")

    elif (message.text == "Восстановление"):
        bot.send_message(message.chat.id, text="Восстоновление с помощью резервной копии была успешна", reply_markup=main)
        shutil.copyfile('copytext.txt','text.txt')
    else:
        bot.send_message(message.chat.id, text="Не понимать")
bot.polling()