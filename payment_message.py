import time
import telebot
from telebot import types
from yoomoney import Quickpay

from keyboards import admin_keyboard, user_keyboard
from database import requests, requests_admin
from config_data.config import Config, load_config

import logging


config: Config = load_config()

admin_id = int(config.tg_bot.admin_ids)

bot = telebot.TeleBot(config.tg_bot.token)
logger = logging.getLogger(__name__)
logging.basicConfig(
        level=logging.INFO,
        # filename="py_log.log",
        # filemode='w',
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
logger.info('Starting bot')
logging.info('on_startup_notify')
date_now = time.strftime("%Y-%m-%d", time.localtime())
time_now = time.strftime("%H:%M:%S", time.localtime())
try:
    text = (f"✅Бот запущен и готов к работе!✅\n"
            f"📅Дата: {date_now}\n"
            f"⏰Время: {time_now}")
    bot.send_message(chat_id=config.tg_bot.support_id, text=text)
except Exception as err:
    logging.exception(err)

def extract_arg(arg):
    return arg.split()[1:]

@bot.message_handler(commands=['start'])
def start(message):
    comand = extract_arg(message.text)
    print(comand)

    logging.info('start')
    user_id = message.from_user.id
    requests.create_table(message)

    if user_id == admin_id:
        markup = admin_keyboard.create_reply_markup_admin()
        bot.send_message(chat_id=message.chat.id,
                         text='Вы являетесь администратором,нажмите на кнопку чтобы выбрать действие',
                         reply_markup=markup)
        bot.register_next_step_handler(message, main_admin)
    if user_id != admin_id:
        markup = user_keyboard.create_start_reply_markup_user()
        bot.send_message(chat_id=message.chat.id,
                         text='Приветсвенное сообщение',
                         reply_markup=markup)
        bot.register_next_step_handler(message, main_user_pay_or_not)


@bot.message_handler(content_types=['text'])
def main_user_pay_or_not(message):
    logging.info('main_user_pay_or_not')
    if message.text == 'Начать':
        user_id = message.from_user.id

        data = requests.check_data_cnt_message(message)
        if (data == []) or (data[0][1] == 0):
            markup = types.InlineKeyboardMarkup()

            quickpay_15 = Quickpay(
                receiver=config.tg_bot.yoomoney_receiver,
                quickpay_form='shop',
                targets='Оплата подписки',
                paymentType='SB',
                sum=2,
                label=f'{user_id}'
            )

            btn1 = types.InlineKeyboardButton(text=f'15 сообщений ({config.tg_bot.tarif_15} рубля)',
                                              url=quickpay_15.base_url)
            markup.add(btn1)

            quickpay_50 = Quickpay(
                receiver=config.tg_bot.yoomoney_receiver,
                quickpay_form='shop',
                targets='Оплата подписки',
                paymentType='SB',
                sum=3,
                label=f'{user_id}'
            )

            btn2 = types.InlineKeyboardButton(text=f'50 сообщений ({config.tg_bot.tarif_50} рубля)',
                                              url=quickpay_50.base_url)
            markup.add(btn2)

            quickpay_100 = Quickpay(
                receiver=config.tg_bot.yoomoney_receiver,
                quickpay_form='shop',
                targets='Оплата подписки',
                paymentType='SB',
                sum=4,
                label=f'{user_id}'
            )

            btn3 = types.InlineKeyboardButton(text=f'100 сообщений ({config.tg_bot.tarif_100} рубля)',
                                              url=quickpay_100.base_url)
            markup.add(btn3)

            quickpay_200 = Quickpay(
                receiver=config.tg_bot.yoomoney_receiver,
                quickpay_form='shop',
                targets='Оплата подписки',
                paymentType='SB',
                sum=5,
                label=f'{user_id}'
            )

            btn4 = types.InlineKeyboardButton(text=f'200 сообщений ({config.tg_bot.tarif_200} рублей)',
                                              url=quickpay_200.base_url)
            markup.add(btn4)
            bot.send_message(chat_id=message.chat.id,
                             text='Чтобы отправлять сообщения в группу вам нужно оплатить подписку',
                             reply_markup=markup)
            time.sleep(3)

            markup_2 = user_keyboard.create_subscribe_verification_markup()

            bot.send_message(chat_id=message.chat.id,
                             text='После оплаты нажмите на кнопку "Опубликовать обьявление"',
                             reply_markup=markup_2)
            bot.register_next_step_handler(message, proverka)

        else:
            markup = user_keyboard.main_menu_buttons()
            bot.send_message(chat_id=message.chat.id,
                             text=f'У вас осталось {data[0][1]} сообщений для отправки',
                             reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Опубликовать обьявление')
def proverka(message):
    logging.info('proverka')
    markup_3 = user_keyboard.create_start_reply_markup_user()
    bot.send_message(message.chat.id, 'Ожидайте,проверяем оплату')

    token = config.tg_bot.yoomoney_access_token
    amount_15 = float(config.tg_bot.tarif_15)
    amount_50 = float(config.tg_bot.tarif_50)
    amount_100 = float(config.tg_bot.tarif_100)
    amount_200 = float(config.tg_bot.tarif_200)
    cnt = requests.proverka(message, token,amount_15,amount_50,amount_100,amount_200)
    if cnt:
        bot.send_message(chat_id=message.chat.id,
                         text=f'Благодарим за оформление подписки,теперь вам доступно {cnt} сообщений\n'
                              f'Чтобы продолжить нажмите на кнопку "Начать"', reply_markup=markup_3)
    else:
        markup = user_keyboard.support_button()
        bot.send_message(chat_id=message.chat.id,
                         text='Оплата не прошла,попробйуте еще раз или обратитесь в поддержку',
                         reply_markup=markup)
        bot.register_next_step_handler(message,main_user_pay_or_not)


@bot.callback_query_handler(func=lambda callback: (callback.data == 'Написать сообщение'))
def main_user(callback):
    logging.info('main_user')
    user_id = callback.from_user.id

    if callback.data == 'Написать сообщение':

        cnt = requests.check_message_cht(user_id)

        if cnt == 0:
            main_user_pay_or_not(callback.message)

        else:
            bot.send_message(chat_id=callback.message.chat.id,
                             text='Отправьте сообщение которое вы хотите опубликовать'
                                  ' (Перед отправкой проверьте сообщение на наличие ошибок и опечаток)')
            bot.register_next_step_handler(callback.message, get_message)


@bot.message_handler(content_types=['text'])
def get_message(message):
    logging.info('get_message')
    user_id = message.from_user.id
    message_to_send = str(message.text)

    if not requests.send_message_to_chat(message_to_send, user_id):
        markup = user_keyboard.support_button()
        bot.send_message(chat_id=message.chat.id,
                         text='Ваше сообщение не прошло модерацию,в нем были найдены стоп слова.\n'
                              'Если в вашем сообщении не было ничего запрещенного обратитесь'
                              ' в поддержку нажав на кнопку ниже',
                         reply_markup=markup)

        markup = user_keyboard.create_start_reply_markup_user()
        bot.send_message(chat_id=message.chat.id,
                         text='Чтобы отправить сообщение еще раз нажмите на кнопку "Начать"',
                         reply_markup=markup)
        bot.register_next_step_handler(message, main_user_pay_or_not)

    else:
        markup = user_keyboard.create_start_reply_markup_user()
        bot.send_message(chat_id=message.chat.id,
                         text='Ваше сообщение прошло модерацию и скоро будет опубликовано',
                         reply_markup=markup)

        # ЗДЕСЬ НУЖНО ПЕРЕДАВАТЬ ПАРАМЕТРЫ ПОЛУЧЕННЫЕ ПРИ ВХОДЕ ПОЛЬЗОВАТЕЛЯ
        bot.send_message(chat_id=chat_id,
                         text=message_to_send)

        bot.register_next_step_handler(message, main_user_pay_or_not)


@bot.message_handler(func=lambda message:(message.text == 'Пополнить список стоп-слов') or (message.text == 'Написать и закрепить пост'))
def main_admin(message):
    logging.info('main_admin')
    if message.text == 'Пополнить список стоп-слов':
        markup = admin_keyboard.create_inline_markup_admin()
        bot.send_message(chat_id=message.chat.id,
                         text='Хотите добавить одно слово или несколько?\n'
                              'Перед отправкой сообщения проверьте правильность написания слова',
                         reply_markup=markup)

    if message.text == 'Написать и закрепить пост':
        bot.send_message(chat_id=message.chat.id,text='Напишите и отправьте текст для поста,текст для кнопки и peer_id чата разделяя их знаками "|"')
        bot.register_next_step_handler(message,create_post)

@bot.callback_query_handler(func=lambda callback: ((callback.data == 'Одно') or (callback.data == 'Несколько')))
def add_words(callback):
    logging.info('add_words')
    if callback.data == 'Одно':
        bot.send_message(chat_id=callback.message.chat.id,
                         text='Введите слово которое хотите добавить в список стоп слов')
        bot.register_next_step_handler(callback.message, one_word)

    if callback.data == 'Несколько':
        bot.send_message(chat_id=callback.message.chat.id,
                         text='Введите стоп слова через запятую')
        bot.register_next_step_handler(callback.message, many_words)


@bot.message_handler(content_types=['text'])
def create_post(message):
    logging.info('create_post')
    data = requests_admin.create_attach_post(message)
    print(data)
    message_to_send = data[0]
    buttun_text = data[1]
    chat_id = int(data[2])
    peer_id = f'https://t.me/Testatstatsbot?start={data[2]}'

    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text=buttun_text,url=f'{peer_id}')
    markup.add(btn)

    sent_message  = bot.send_message(chat_id=chat_id,text=message_to_send,reply_markup=markup)
    bot.pin_chat_message(chat_id,sent_message.message_id)

def one_word(message):
    logging.info('one_word')
    markup = admin_keyboard.create_reply_markup_admin()
    requests_admin.get_one_word(message)
    bot.send_message(chat_id=message.chat.id,
                     text='Стоп слово добавлено',
                     reply_markup=markup)
    bot.register_next_step_handler(message, main_admin)


def many_words(message):
    logging.info('many_words')
    markup = admin_keyboard.create_reply_markup_admin()
    requests_admin.get_many_words(message)
    bot.send_message(chat_id=message.chat.id,
                     text='Стоп слова добавлены',
                     reply_markup=markup)
    bot.register_next_step_handler(message, main_admin)


bot.polling(none_stop=True)
