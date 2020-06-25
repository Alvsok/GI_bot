import telebot
import os
from dotenv import load_dotenv
from gi_data import di, anti_di, syn_di

load_dotenv()


def anti_words(word, sss):
    if anti_di.get(word) is None:
        return True
    for elem in anti_di[word]:
        if elem in sss:
            return False
    return True


def print_str(arr):
    res_str = ''
    arr.sort()
    for elem in arr:
        res_str += print_emoji(elem[0]) + elem[1] + '\t' + str(elem[0]) + '\n'
    return res_str


def print_emoji(n):
    if n < 50:
        return '\U0001F7E9'
    elif 50 <= n < 70:
        return '\U0001F7E8'
    else:
        return '\U0001F7E5'


def word_in_di(word, di):
    for elem in list(di):
        if word in elem:
            return True
    return False


TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    hello_txt = 'Напечатай полное или сокращенное название продукта - '
    hello_txt += 'я постараюсь найти его гликемический индекс.'
    bot.send_message(message.chat.id, hello_txt)


@bot.message_handler(content_types=['text'])
def text_handler(message):
    res_arr = []
    text_full = message.text.lower()

    if len(text_full) > 5:
        text1 = text_full[:5]
        if word_in_di(text1, syn_di):
            text = syn_di[text1]
        else:
            text = text1
    else:
        text = text_full

    chat_id = message.chat.id
    for elem in di:
        if text in elem and anti_words(text, elem):
            res_arr.append((di[elem], elem))
    if res_arr == []:
        bot.send_message(chat_id, 'Простите, я не знаю ГИ этого продукта :(')
    else:
        res = print_str(res_arr)
        bot.send_message(chat_id, res)


bot.polling(none_stop=True)
