from telebot import types


def create_start_reply_markup_user():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton(text='Тарифы')
    markup.add(btn)
    return markup


def create_post_message_user():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton('Написать сообщение')
    markup.add(btn)
    return markup


def create_subscribe_verification_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton(text='Опубликовать объявление')
    markup.add(btn)
    return markup


def main_menu_buttons():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Чат с поддержкой', callback_data='support')
    btn2 = types.InlineKeyboardButton(text='Написать сообщение', callback_data='write_message')
    markup.add(btn2)
    markup.add(btn1)
    return markup


def support_button():
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text='Чат с поддержкой',callback_data='support')
    markup.add(btn)
    return markup
