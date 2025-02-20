from telebot import types


def create_start_reply_markup_user():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton(text='Тарифы')
    markup.add(btn)
    return markup

def check_pay_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton('Проверить оплату')
    markup.add(btn)
    return markup


def create_post_message_user():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton('Написать сообщение')
    markup.add(btn)
    return markup


def create_subscribe_verification_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton(text='Начать публикацию')
    markup.add(btn)
    return markup


def main_menu_buttons():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Чат с поддержкой', callback_data='Поддержка')
    btn2 = types.InlineKeyboardButton(text='Написать сообщение', callback_data='write_message')
    markup.add(btn2)
    markup.add(btn1)
    return markup


def support_button():
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text='Чат с поддержкой',callback_data='Поддержка')
    markup.add(btn)
    return markup

def add_photo_or_video_buttons(user_id):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Добавить фото',callback_data=f'Добавить фото {user_id}')
    btn2 = types.InlineKeyboardButton('Добавить видео',callback_data=f'Добавить видео {user_id}')
    markup.add(btn1,btn2)
    btn4 = types.InlineKeyboardButton('Редактировать текст',callback_data=f'Редактировать текст {user_id}')
    markup.add(btn4)
    btn3 = types.InlineKeyboardButton('Опубликовать обьявление', callback_data=f'Опубликовать обьявление {user_id}')
    markup.add(btn3)
    return markup

def pre_send_post_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton('Предварительный просмотр')
    markup.add(btn)
    return markup