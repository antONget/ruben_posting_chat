import time
import telebot
from telebot import types
from yoomoney import Quickpay
import sqlite3

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

    conn = sqlite3.connect('database/USERS.sql')
    cur = conn.cursor()
    cur.execute(f'UPDATE user_{user_id} SET id = "{user_id}"')
    # cur.execute(f'UPDATE user_{user_id} SET message_cnt = "{50}"')
    conn.commit()
    cur.close()
    conn.close()



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
    bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.message_id,
                          text='Если у вас есть вопросы связанные с работой бота, либо проблемы с проведением платежа, то можете обратиться к нам,'
                               'также будем рады услышать предложения по улучшению функционала бота.'
                               '\n@Mnenie_Ru'
                               '\n@Alextreide84',reply_markup=None)

@bot.message_handler(func=lambda message: (message.text == 'Начать публикацию'))
def main_user_pay_or_not(message):
    logging.info('main_user_pay_or_not')
    if message.text == 'Начать публикацию':
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

            markup_2 = user_keyboard.check_pay_button()

            bot.send_message(chat_id=message.chat.id,
                             text='После оплаты нажмите на кнопку "Проверить оплату"',
                             reply_markup=markup_2)
            bot.register_next_step_handler(message, proverka)

        else:
            markup = user_keyboard.main_menu_buttons()
            bot.send_message(chat_id=message.chat.id,
                             text=f'У вас осталось {data[0][1]} сообщений для отправки\n'
                                  f'Для публикации нажмите <b>"Написать сообщение"</b>\n'
                                  f'Если у вас есть вопросы, задайте их в поддержку по кнопке <b>"Чат с поддержкой"</b>',
                             reply_markup=markup,parse_mode='HTML')


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
                              f'Чтобы продолжить нажмите на кнопку "Начать публикацию"', reply_markup=markup_3)
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
    if message_to_send == 'Начать публикацию':
        main_user_pay_or_not(message)

    else:

        if not requests.send_message_to_chat(message_to_send, user_id):
            markup = user_keyboard.support_button()
            bot.send_message(chat_id=message.chat.id,
                             text='Ваше сообщение не прошло модерацию,в нем были найдены стоп слова.\n'
                                  'Если в вашем сообщении не было ничего запрещенного обратитесь'
                                  ' в поддержку нажав на кнопку ниже',
                             reply_markup=markup)

            markup = user_keyboard.create_subscribe_verification_markup()
            bot.send_message(chat_id=message.chat.id,
                             text='Чтобы отправить сообщение еще раз нажмите на кнопку "Начать публикацию"',
                             reply_markup=markup)
            bot.register_next_step_handler(message, main_user_pay_or_not)
        else:
            media_data = requests.get_media(user_id)
            if str(media_data) == 'None':
                markup = user_keyboard.add_photo_or_video_buttons(user_id)
                bot.send_message(chat_id=message.chat.id,
                                     text=f'Ваше сообщение прошло модерацию\n\nВы можете добавить фото или видео а также отретактировать ваше сообщение \n\nваше текущее обьявление выглядит так: {message_to_send}\n\n'
                                          f'Если все заполнено корректно, а фотографий быть не должно то нажмите на кнопку "Опубликовать обьявление"',
                                     reply_markup=markup)
                requests.save_message_to_send(message_to_send,user_id)
            else:
                requests.save_message_to_send(message_to_send, user_id)
                pre_post(message)

@bot.callback_query_handler(func=lambda callback:('Добавить фото' in callback.data) or ('Добавить видео' in callback.data) or ('Опубликовать обьявление' in callback.data) or ('Редактировать текст' in callback.data))
def redact_or_send_post(callback):
    user_id = callback.from_user.id

    if callback.data == f'Добавить фото {user_id}':
        bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.message_id,text='Отправьте одно фото дня добавления к посту\n\nПосле отправки нажмите на кнопку "Предварительный просмотр"',reply_markup=None)

    if callback.data == f'Добавить видео {user_id}':
        bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.message_id,text='Отправьте одно видео для добавления его к посту\n\nПосле отправки нажмите на кнопку "Предварительный просмотр"',reply_markup=None)

    if callback.data == f'Опубликовать обьявление {user_id}':
        chat_id = requests.get_chat_id(user_id)

        if str(chat_id) != 'None':
            link_name_data = requests.get_group_name_by_id(chat_id)

            name = link_name_data[0][0]
            link = str(link_name_data[0][2])

            while ' ' in link:
                link = link.replace(' ','')

            message_to_send = str(requests.get_message_to_send(user_id)[0][0]) + f'\n📣 <code>Объявление размещено пользователем в группе:</code> <a href="{link}">{name}\nПодпишись!!!</a> ✔️'

        else:
            message_to_send = str(requests.get_message_to_send(user_id)[0][0]) + (f'\n'
                                                                                  f'📣 <code>Объявление размещено пользователем в группах:</code> <a href="https://t.me/raznorabochie_Vsevologsk">Разнорабочие Всеволожск🛠️</a>\n'
                                                                                    f' <a href="https://t.me/sam_o_stroy">Самострой 🏡</a>!!! ✔️')

        data = requests.get_media(user_id).split('|')

        media_files = []

        try:
            if data[0].split(':')[0] == 'photo':
                media_files.append(types.InputMediaPhoto(data[0].split(':')[1], caption=message_to_send,parse_mode='HTML'))

            else:
                media_files.append(types.InputMediaVideo(data[0].split(':')[1], caption=message_to_send,parse_mode='HTML'))

            for elem_id in data[1:]:
                if elem_id.split(':')[0] == 'photo':
                    media_files.append(types.InputMediaPhoto(elem_id.split(':')[1]))

                if elem_id.split(':')[0] == 'video':
                    media_files.append(types.InputMediaVideo(elem_id.split(':')[1]))

        except IndexError as e:
            media_files = []


        if str(chat_id) != 'None':
            if media_files != []:
                bot.send_media_group(chat_id,media_files)

                requests.del_one_message(user_id)
                requests.clean_media_files(user_id)

                bot.send_message(callback.message.chat.id,'Ваше обьявление скоро будет опубликовано',reply_markup=user_keyboard.create_subscribe_verification_markup())

                bot.register_next_step_handler(callback.message, main_user_pay_or_not)

            else:
                bot.send_message(chat_id=chat_id,text=message_to_send,parse_mode='HTML')

                requests.del_one_message(user_id)
                requests.clean_media_files(user_id)

                bot.send_message(callback.message.chat.id, 'Ваше обьявление скоро будет опубликовано',
                                 reply_markup=user_keyboard.create_subscribe_verification_markup())

                bot.register_next_step_handler(callback.message, main_user_pay_or_not)


        else:
            if media_files != []:
                ids = str(config.tg_bot.chat_id).split(',')
                for chat_id in ids:
                    if chat_id == '':
                        continue
                    else:
                        bot.send_media_group(int(chat_id),media_files)

                requests.del_one_message(user_id)
                requests.clean_media_files(user_id)

                bot.send_message(callback.message.chat.id, 'Ваше обьявление скоро будет опубликовано',
                                 reply_markup=user_keyboard.create_subscribe_verification_markup())

                bot.register_next_step_handler(callback.message, main_user_pay_or_not)

            else:
                ids = str(config.tg_bot.chat_id).split(',')
                for chat_id in ids:
                    if chat_id == '':
                        continue
                    else:
                        bot.send_message(chat_id=chat_id,text=message_to_send,parse_mode='HTML')

                requests.del_one_message(user_id)
                requests.clean_media_files(user_id)

                bot.send_message(callback.message.chat.id, 'Ваше обьявление скоро будет опубликовано',
                                 reply_markup=user_keyboard.create_subscribe_verification_markup())

                bot.register_next_step_handler(callback.message, main_user_pay_or_not)



    if callback.data == f'Редактировать текст {user_id}':
        bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.message_id,text='Отправьте новый текст',reply_markup=None)
        bot.register_next_step_handler(callback.message,get_message)

@bot.message_handler(content_types=['photo'])
def get_photo_to_post(message):
    user_id = message.from_user.id
    photo_ids = []

    for index ,photo in enumerate(message.photo):
        if index%4 == 0:
            id = photo.file_id
            photo_ids.append(id)

    media_data = requests.get_media(user_id)

    photo_id = photo_ids[0]
    new_media = ''
    if str(media_data) == 'None':
        new_media = f'photo:{photo_id}' + '|'
    else:
        new_media = media_data + f'photo:{photo_id}' + '|'
    requests.update_media_files(user_id,new_media)
    bot.send_message(message.chat.id, 'Фото добавлено,можете добавить еще',reply_markup=user_keyboard.pre_send_post_button())


@bot.message_handler(content_types=['video'])
def get_video_to_post(message):
    user_id = message.from_user.id

    video_ids = []

    video_ids.append(message.video.file_id)

    media_data = requests.get_media(user_id)
    for video_id in video_ids:
        media_data += f'video:{video_id}' + '|'

    requests.update_media_files(user_id, media_data)
    bot.send_message(message.chat.id, 'Видео добавлено, можете добавить еще',reply_markup=user_keyboard.pre_send_post_button())


@bot.message_handler(func=lambda message:(message.text == 'Предварительный просмотр'))
def pre_post(message):
    user_id = message.from_user.id

    data = requests.get_media(user_id).split('|')

    media_files = []
    message_to_send = str(requests.get_message_to_send(user_id)[0][0])

    if data[0].split(':')[0] == 'photo':
        media_files.append(types.InputMediaPhoto(data[0].split(':')[1],caption=message_to_send))

    else:
        media_files.append(types.InputMediaVideo(data[0].split(':')[1],caption=message_to_send))

    # print(data)
    for elem_id in data[1:]:
        if elem_id.split(':')[0] == 'photo':
            media_files.append(types.InputMediaPhoto(elem_id.split(':')[1]))
            # print(1)

        if elem_id.split(':')[0] == 'video':
            media_files.append(types.InputMediaVideo(elem_id.split(':')[1]))

    bot.send_media_group(message.chat.id,media_files)
    bot.send_message(message.chat.id,f'ваше текущее обьявление выглядит так\n\nВыберите действие',reply_markup=user_keyboard.add_photo_or_video_buttons(user_id))




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
                              ' , peer_id чата, ссылку на группу и название группы разделяя их знаками "|" (peer_id группы вы можете получить с помощью'
                              ' бота @username_to_id_bot\n'
                              'Например: <code>Разместить объявление в группу вы можете через бота | Объявление |'
                              ' -1002454315455 | https://t.me/example_link | Самострой</code>',
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
        peer_id = f'https://t.me/{config.tg_bot.bot_link_name}?start={data[2]}'
        href = str(data[3])
        group_name = str(data[4])
        requests_admin.add_name_and_id_group(group_name,
                                             chat_id,
                                             href)

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
            print(e)
            bot.send_message(message.chat.id,
                             'Неправильно указан peer_id чата либо бот не является администратором чата, '
                             'попробуйте вести сообщение еще раз')
            bot.register_next_step_handler(message, create_post)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id,
                         'Данные введены неверно,повторно нажмите на кнопку и повторите попытку')



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


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        time.sleep(2)
