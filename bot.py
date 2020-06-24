import telebot
import os
from dotenv import load_dotenv
from gi_data import di, anti_di

load_dotenv()


def anti_words(word, sss):
    if anti_di.get(word) is None:
        return True
    for elem in anti_di[word]:
        if elem in sss:
            return False
    return True


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
    text_full = message.text.lower()

    if len(text_full) > 5:
        text = text_full[:5]
    else:
        text = text_full

    chat_id = message.chat.id
    for elem in di:
        if text in elem and anti_words(text, elem):
            res += str(elem) + ' ' + str(di[elem]) + '\n'
    if res == '':
        bot.send_message(chat_id, 'Простите, не знаю такой продукт :(')
    else:
        bot.send_message(chat_id, res)


bot.polling(none_stop=True)
