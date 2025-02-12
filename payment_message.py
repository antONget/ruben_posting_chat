import time
import telebot
from telebot import types
from yoomoney import Quickpay

from keyboards import admin_keyboard, user_keyboard
from database import requests, requests_admin
from config_data.config import Config, load_config

import logging
waiting_message_admin = False

config: Config = load_config()

admin_ids = str(config.tg_bot.admin_ids)
admin_ids_list = admin_ids.split(',')

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
    logging.info('start')
    comand = extract_arg(message.text)


    logging.info('start')
    user_id = message.from_user.id
    requests.create_table(message)
    if str(user_id) in admin_ids_list:
        markup = admin_keyboard.create_reply_markup_admin()
        bot.send_message(chat_id=message.chat.id,
                         text='Вы являетесь администратором,нажмите на кнопку чтобы выбрать действие',
                         reply_markup=markup)
        bot.register_next_step_handler(message, main_admin)
    if str(user_id) not in admin_ids_list:
        if not comand:
            markup = user_keyboard.create_subscribe_verification_markup()
            bot.send_message(chat_id=message.chat.id,
                             text='Привет! 🎉\n\nДобро пожаловать в наш Телеграм-бот для публикации объявлений! Здесь вы можете легко и '
                                  'быстро разместить свои объявления в нашей группе по подписке. \n\n🌟Чтобы начать, просто следуйте'
                                  ' инструкциям и отправьте ваше объявление. Мы поможем вам донести информацию до нашей аудитории! '
                                  '📣\n\nЕсли у вас есть вопросы или нужно больше информации, просто напишите нам. Мы всегда готовы помочь! 🤗\n\nУдачи с вашими объявлениями! 🚀')
            bot.send_message(chat_id=message.chat.id, text='Вы перешли в бота по прямой ссылке и ваше сообщения будут'
                                                           ' публиковаться в эти группы:\n'
                                                           '1. @sam_o_stroy\n'
                                                           '2. @raznorabochie_Vsevologhsk\n'
                                                           'Чтобы сообщения публиковались только в одну группу'
                                                           ' перейдите в чат и зайдите в бота по ссылке в'
                                                           ' закрепленном сообщении',
                             reply_markup=markup)
            requests.add_chat_id_user(user_id, 'None')
        else:
            requests.add_chat_id_user(user_id, comand[0])
            markup_4 = user_keyboard.create_subscribe_verification_markup()
            bot.send_message(chat_id=message.chat.id,
                             text='Привет! 🎉\n\nДобро пожаловать в наш Телеграм-бот для публикации объявлений! Здесь вы можете легко и '
                                  'быстро разместить свои объявления в нашей группе по подписке. \n\n🌟Чтобы начать, просто следуйте'
                                  ' инструкциям и отправьте ваше объявление. Мы поможем вам донести информацию до нашей аудитории! '
                                  '📣\n\nЕсли у вас есть вопросы или нужно больше информации, просто напишите нам. Мы всегда готовы помочь! 🤗\n\nУдачи с вашими объявлениями! 🚀',
                             reply_markup=markup_4)

@bot.callback_query_handler(func=lambda callback:(callback.data == 'Поддержка'))
def support(callback):
    bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.chat.id,
                          text='Если у вас есть вопросы связанные с работой бота, либо проблемы с проведением платежа, то можете обратиться к нам,'
                               'также будем рады услышать предложения по улучшению функционала бота.'
                               '\n@Mnenie_Ru'
                               '\n@Alextreide84',reply_markup=types.InlineKeyboardMarkup())

@bot.message_handler(func=lambda message: (message.text == 'Опубликовать объявление'))
def main_user_pay_or_not(message):
    logging.info('main_user_pay_or_not')
    if message.text == 'Опубликовать объявление':
        user_id = message.from_user.id

        data = requests.check_data_cnt_message(message)
        if (data[0][1] is None) or (data[0][1] == 0):
            markup = types.InlineKeyboardMarkup()

            quickpay_1 = Quickpay(
                receiver=config.tg_bot.yoomoney_receiver,
                quickpay_form='shop',
                targets='Оплата подписки',
                paymentType='SB',
                sum=config.tg_bot.tarif_1,
                label=f'{user_id}'
            )

            btn1 = types.InlineKeyboardButton(text=f'1 сообщение ({config.tg_bot.tarif_1} рублей)',
                                              url=quickpay_1.base_url)
            markup.add(btn1)

            quickpay_5 = Quickpay(
                receiver=config.tg_bot.yoomoney_receiver,
                quickpay_form='shop',
                targets='Оплата подписки',
                paymentType='SB',
                sum=config.tg_bot.tarif_5,
                label=f'{user_id}'
            )

            btn2 = types.InlineKeyboardButton(text=f'5 сообщений ({config.tg_bot.tarif_5} рубля)',
                                              url=quickpay_5.base_url)
            markup.add(btn2)

            quickpay_10 = Quickpay(
                receiver=config.tg_bot.yoomoney_receiver,
                quickpay_form='shop',
                targets='Оплата подписки',
                paymentType='SB',
                sum=config.tg_bot.tarif_10,
                label=f'{user_id}'
            )

            btn3 = types.InlineKeyboardButton(text=f'10 сообщений ({config.tg_bot.tarif_10} рубля)',
                                              url=quickpay_10.base_url)
            markup.add(btn3)

            quickpay_50 = Quickpay(
                receiver=config.tg_bot.yoomoney_receiver,
                quickpay_form='shop',
                targets='Оплата подписки',
                paymentType='SB',
                sum=config.tg_bot.tarif_50,
                label=f'{user_id}'
            )

            btn4 = types.InlineKeyboardButton(text=f'50 сообщений ({config.tg_bot.tarif_50} рублей)',
                                              url=quickpay_50.base_url)
            markup.add(btn4)
            bot.send_message(chat_id=message.chat.id,
                             text='Чтобы отправлять сообщения в группу вам нужно оплатить подписку',
                             reply_markup=markup)
            time.sleep(3)

            markup_2 = user_keyboard.create_post_message_user()

            bot.send_message(chat_id=message.chat.id,
                             text='После оплаты нажмите на кнопку "Проверить оплату"',
                             reply_markup=markup_2)
            bot.register_next_step_handler(message, proverka)

        else:
            markup = user_keyboard.main_menu_buttons()
            bot.send_message(chat_id=message.chat.id,
                             text=f'У вас осталось {data[0][1]} сообщений для отправки',
                             reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Проверить оплату')
def proverka(message):
    logging.info('proverka')
    markup_3 = user_keyboard.create_subscribe_verification_markup()
    bot.send_message(message.chat.id, 'Ожидайте,проверяем оплату')

    token = config.tg_bot.yoomoney_access_token
    amount_1 = float(config.tg_bot.tarif_1)
    amount_5 = float(config.tg_bot.tarif_5)
    amount_10 = float(config.tg_bot.tarif_10)
    amount_50 = float(config.tg_bot.tarif_50)
    cnt = requests.proverka(message, token, amount_1, amount_5, amount_10, amount_50)
    if cnt:
        bot.send_message(chat_id=message.chat.id,
                         text=f'Благодарим за оформление подписки,теперь вам доступно {cnt} сообщений\n'
                              f'Чтобы продолжить нажмите на кнопку "Опубликовать объявление"', reply_markup=markup_3)
    else:
        markup = user_keyboard.support_button()
        bot.send_message(chat_id=message.chat.id,
                         text='Оплата не прошла,попробуйте еще раз или обратитесь в поддержку',
                         reply_markup=markup)
        bot.register_next_step_handler(message, proverka)


@bot.callback_query_handler(func=lambda callback: (callback.data == 'write_message'))
def main_user(callback):
    logging.info('main_user')
    user_id = callback.from_user.id

    if callback.data == 'write_message':

        cnt = requests.check_message_cht(user_id)

        if cnt == 0:
            main_user_pay_or_not(callback.message)

        else:
            bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.message_id,
                                  text='Отправьте сообщение которое вы хотите опубликовать'
                                       ' (Перед отправкой проверьте сообщение на наличие ошибок и опечаток)',
                                  reply_markup=types.InlineKeyboardMarkup())
            bot.register_next_step_handler(callback.message, get_message)


@bot.message_handler(func=lambda message: False)
def get_message(message):
    logging.info('get_message')
    user_id = message.from_user.id
    message_to_send = str(message.text)
    chat_id = requests.get_chat_id(user_id)

    if not requests.send_message_to_chat(message_to_send, user_id):
        markup = user_keyboard.support_button()
        bot.send_message(chat_id=message.chat.id,
                         text='Ваше сообщение не прошло модерацию,в нем были найдены стоп слова.\n'
                              'Если в вашем сообщении не было ничего запрещенного обратитесь'
                              ' в поддержку нажав на кнопку ниже',
                         reply_markup=markup)

        markup = user_keyboard.create_subscribe_verification_markup()
        bot.send_message(chat_id=message.chat.id,
                         text='Чтобы отправить сообщение еще раз нажмите на кнопку "Опубликовать объявление"',
                         reply_markup=markup)
        bot.register_next_step_handler(message, main_user_pay_or_not)
    else:
        if str(chat_id) != 'None':
            markup = user_keyboard.create_subscribe_verification_markup()
            bot.send_message(chat_id=message.chat.id,
                             text='Ваше сообщение прошло модерацию и скоро будет опубликовано',
                             reply_markup=markup)
            bot.send_message(chat_id=chat_id,
                             text=message_to_send)
            bot.register_next_step_handler(message, main_user_pay_or_not)

        else:
            markup = user_keyboard.create_subscribe_verification_markup()
            bot.send_message(chat_id=message.chat.id,
                             text='Ваше сообщение прошло модерацию и скоро будет опубликовано',
                             reply_markup=markup)

            ids = str(config.tg_bot.chat_id).split(',')
            for chat_id in ids:
                bot.send_message(chat_id=int(chat_id), text=message_to_send)
            bot.register_next_step_handler(message, main_user_pay_or_not)


@bot.message_handler(func=lambda message:(message.text == 'Пополнить список стоп-слов') or
                                         (message.text == 'Написать и закрепить пост') or (
    message.text == 'Просмотреть список стоп слов') or (message.text == 'Удалить список стоп слов'))
def main_admin(message):
    logging.info('main_admin')
    if message.text == 'Пополнить список стоп-слов':
        markup = admin_keyboard.create_inline_markup_admin()
        bot.send_message(chat_id=message.chat.id,
                         text='Хотите добавить одно слово или несколько?\n'
                              'Перед отправкой сообщения проверьте правильность написания слова',
                         reply_markup=markup)

    if message.text == 'Написать и закрепить пост':
        bot.send_message(chat_id=message.chat.id,
                         text='Напишите и отправьте текст для поста,текст для кнопки'
                              ' и peer_id чата разделяя их знаками "|" (peer_id группы вы можете получить с помощью'
                              ' бота @username_to_id_bot\n'
                              'Например: <code>Разместить объявление в группу вы можете через бота | Объявление |'
                              ' -1002130733166</code>',
                         parse_mode='html')
        bot.register_next_step_handler(message,create_post)

    if message.text == 'Просмотреть список стоп слов':
        words = requests_admin.get_all_stop_words()
        bot.send_message(chat_id=message.chat.id,text=words)

    if message.text == 'Удалить список стоп слов':
        result = requests_admin.delete_all_stop_words()
        if result:
            bot.send_message(chat_id=message.chat.id,
                             text='Список стоп слов очищен')
        else:
            bot.send_message(chat_id=message.chat.id,
                             text='Произошла ошибка')


@bot.callback_query_handler(func=lambda callback: ((callback.data == 'Одно') or
                                                   (callback.data == 'Несколько')))
def add_words(callback):
    global waiting_message_admin
    logging.info('add_words')
    if callback.data == 'Одно':
        bot.send_message(chat_id=callback.message.chat.id,
                         text='Введите слово которое хотите добавить в список стоп слов')
        bot.register_next_step_handler(callback.message, one_word)
        waiting_message_admin = True

    if callback.data == 'Несколько':
        bot.send_message(chat_id=callback.message.chat.id,
                         text='Введите стоп слова через запятую')
        bot.register_next_step_handler(callback.message, many_words)
        waiting_message_admin = True


@bot.message_handler(func=lambda message: waiting_message_admin)
def create_post(message):
    global waiting_message_admin
    logging.info('create_post')
    try:
        data = requests_admin.create_attach_post(message)
        message_to_send = data[0]
        buttun_text = data[1]
        chat_id = int(data[2])
        peer_id = f'https://t.me/Sampostroy_bot?start={data[2]}'

        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text=buttun_text,
                                         url=f'{peer_id}')
        markup.add(btn)
        try:
            sent_message = bot.send_message(chat_id=chat_id,text=message_to_send,reply_markup=markup)
            bot.pin_chat_message(chat_id=chat_id,
                                 message_id=sent_message.message_id)
            bot.register_next_step_handler(message, main_admin)
            waiting_message_admin = False

        except Exception as e:
            bot.send_message(message.chat.id, 'Неправильно указан peer_id чата либо бот не является администратором чата,попробуйте вести сообщение еще раз')
            bot.register_next_step_handler(message, create_post)
    except Exception as e:
        bot.send_message(message.chat.id,'Данные Введеные неверно,повторно нажмите на кнопку и повторите попытку')



def one_word(message):
    global waiting_message_admin
    logging.info('one_word')
    markup = admin_keyboard.create_reply_markup_admin()
    requests_admin.get_one_word(message)
    bot.send_message(chat_id=message.chat.id,
                     text='Стоп слово добавлено',
                     reply_markup=markup)
    bot.register_next_step_handler(message, main_admin)
    waiting_message_admin = False


def many_words(message):
    global waiting_message_admin
    logging.info('many_words')
    markup = admin_keyboard.create_reply_markup_admin()
    requests_admin.get_many_words(message)
    bot.send_message(chat_id=message.chat.id,
                     text='Стоп слова добавлены',
                     reply_markup=markup)
    bot.register_next_step_handler(message, main_admin)
    waiting_message_admin = False


bot.polling(none_stop=True)
