import telebot
import os
from dotenv import load_dotenv
from gi_data import di

load_dotenv()


TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    hello_txt = 'Напечатай полное или сокращенное название продукта - '
    hello_txt += 'я постараюсь найти его гликемический индекс.'
    bot.send_message(message.chat.id, hello_txt)


@bot.message_handler(content_types=['text'])
def text_handler(message):
    res = ''
    text = message.text.lower()
    chat_id = message.chat.id
    for elem in di:
        if text in elem:
            res += str(elem) + ' ' + str(di[elem]) + '\n'
    if res == '':
        bot.send_message(chat_id, 'Простите, не знаю такой продукт :(')
    else:
        bot.send_message(chat_id, res)


bot.polling(none_stop=True)
