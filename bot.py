import telebot
from telebot import types
import os
from dotenv import load_dotenv
from gi_data import di, anti_di, syn_di

load_dotenv()


def print_str(arr):
    res_str = ''
    arr.sort()
    for elem in arr:
        res_str += print_emoji(elem[0]) + elem[1] + ' ' + str(elem[0]) + '\n'
    return res_str


def print_emoji(n):
    if n < 50:
        return '\U0001F7E9'
    elif 50 <= n < 70:
        return '\U0001F7E8'
    else:
        return '\U0001F7E5'


def w1_ok_with_w2(word1, word2):

    for elem in list(anti_di):
        if word1 in elem:
            for elem2 in anti_di[elem]:
                if elem2 in word2:
                    return False
    return True


def word_in_di(word, di):
    for elem in list(di):
        if word in elem:
            return (True, di[elem])
    return (False, [])


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
    chat_id = message.chat.id

    if len(text_full) > 4:
        text1 = text_full[:5]
        # проверка на синонимы
        if word_in_di(text1, syn_di)[0]:
            text = word_in_di(text1, syn_di)[1]
        else:
            text = text1
    else:
        text = text_full

    for elem in list(di):
        if text in elem and w1_ok_with_w2(text, elem):
            res_arr.append((di[elem], elem))

    if res_arr == []:
        bot.send_message(chat_id, 'Простите, я не знаю ГИ этого продукта :(')
    else:
        res = print_str(res_arr)
        bot.send_message(chat_id, res)

        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(
            text='Рецепт здоровой кухни', url='https://alsok.org/')
        keyboard.add(url_button)
        bot.send_message(
            message.chat.id,
            #    'Нажми на кнопку и узнай',
            reply_markup=keyboard
        )


'''
@bot.message_handler(commands=['url'])
def url(message):
    markup = types.InlineKeyboardMarkup()
    btn_my_site = types.InlineKeyboardButton(
        text='Наш сайт', url='https://alsok.org/')
    markup.add(btn_my_site)
    bot.send_message(
        message.chat.id,
        "Нажми на кнопку и перейди на наш сайт.",
        reply_markup=markup
    )



@bot.message_handler(content_types=['text'])
def default_test(message):
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(
        text='Перейти', url='https://alsok.org/')
    keyboard.add(url_button)
    bot.send_message(
        message.chat.id,
        "Привет! Нажми на кнопку и перейди в Alsok.",
        reply_markup=keyboard
    )
'''

bot.polling(none_stop=True)
