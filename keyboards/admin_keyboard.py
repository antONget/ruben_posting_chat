from telebot import types


def create_reply_markup_admin():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text='Пополнить список стоп-слов')
    btn2 = types.KeyboardButton(text='Написать и закрепить пост')
    btn3 = types.KeyboardButton(text='Просмотреть список стоп слов')
    btn4 = types.KeyboardButton(text='Удалить список стоп слов')
    markup.add(btn1,btn2)
    markup.add(btn3,btn4)
    return markup


def create_inline_markup_admin():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Одно слово', callback_data='Одно')
    markup.add(btn1)
    btn2 = types.InlineKeyboardButton(text='Несколько', callback_data='Несколько')
    markup.add(btn2)
    return markup
