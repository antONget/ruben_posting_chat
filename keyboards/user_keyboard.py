from telebot import types


def create_start_reply_markup_user():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton(text='Начать')
    markup.add(btn)
    return markup


def create_subscribe_verification_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton(text='Опубликовать обьявление')
    markup.add(btn)
    return markup


def main_menu_buttons():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Чат с поддержкой', url='https://t.me/AntonPon0marev')
    btn2 = types.InlineKeyboardButton(text='Написать сообщение', callback_data='Написать сообщение')
    markup.add(btn2)
    markup.add(btn1)
    return markup


def support_button():
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text='Чат с поддержкой', url='https://t.me/AntonPon0marev')
    markup.add(btn)
    return markup
