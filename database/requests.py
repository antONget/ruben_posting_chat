import sqlite3
from yoomoney import Client
import logging


def create_table(message):
    logging.info('create_table')
    # СОЗДАНИЕ БД ЕСЛИ ОНИ ЕЩЕ НЕ СОЗДАНЫ
    user_id = message.from_user.id

    conn = sqlite3.connect('database/BAD_WORDS.sql')
    cur = conn.cursor()
    cur.execute(f'CREATE TABLE IF NOT EXISTS bad_words (word text)')
    conn.commit()
    cur.close()
    conn.close()

    conn = sqlite3.connect('database/USERS.sql')
    cur = conn.cursor()
    cur.execute(f'CREATE TABLE IF NOT EXISTS user_{user_id} (id int,message_cnt int,chats_id text,message_to_send text,media_files text)')
    conn.commit()
    cur.close()
    conn.close()

    conn = sqlite3.connect('database/GROUP_NAME.sql')
    cur = conn.cursor()
    cur.execute(f'CREATE TABLE IF NOT EXISTS group_name (name text , id int,href text)')
    conn.commit()
    cur.close()
    conn.close()

def add_chat_id_user(user_id, chat_id):
    conn = sqlite3.connect('database/USERS.sql')
    cur = conn.cursor()
    cur.execute(f'SELECT chats_id FROM user_{user_id}')
    ids = cur.fetchall()
    if not ids:
        cur.execute(f'INSERT INTO user_{user_id} (chats_id) VALUES ("{chat_id}")')
    else:
        cur.execute(f'UPDATE user_{user_id} SET chats_id = "{chat_id}"')
    conn.commit()
    cur.close()
    conn.close()


# ДОБАВЛЕНИЕ СТОП-СЛОВ
def get_one_word(message):
    logging.info('get_one_word')
    word = message.text
    # ОДНО СЛОВО
    conn = sqlite3.connect('database/BAD_WORDS.sql')
    cur = conn.cursor()
    cur.execute(f'INSERT INTO bad_words (word) VALUES ("{word}")')
    conn.commit()
    cur.close()
    cur.close()


def get_many_words(message):
    logging.info('get_many_words')
    words = str(message.text)
    word_list = words.split(',')
    # НЕСКОЛЬКО СЛОВ
    conn = sqlite3.connect('database/BAD_WORDS.sql')
    cur = conn.cursor()

    for word in word_list:
        cur.execute(f'INSERT INTO bad_words (word) VALUES ("{word}")')
        conn.commit()

    cur.close()
    conn.close()


def delete_one_word(message):
    logging.info('delete_one_word')
    user_id = message.from_user.id
    # ВЫЧИТАНИЕ ОДНОГО СЛОВА ИЗ ЛИМТА СООБЩЕНИЙ ПРИ ОТПРАВКЕ СООБЩЕНИИЯ
    conn = sqlite3.connect('database/USERS.sql')
    cur = conn.cursor()
    cur.execute(f'SELECT message_cnt FROM user_{user_id}')
    data = cur.fetchall()
    cnt = data[0][0] - 1
    cur.execute(f'UPDATE user_{user_id} SET message_cnt = "{cnt}"')
    conn.commit()
    cur.close()
    conn.close()


# ПРОВЕРКА ОПЛАТЫ И ЗАПИСЬ В БД КОЛ-ВА СЛОВ (ПО ПОДПИСКЕ)
def proverka(message, token, amount_1, amount_5, amount_10, amount_50):
    logging.info('proverka')
    PAYMENT_TOKEN = token

    user_id = message.from_user.id

    client = Client(PAYMENT_TOKEN)
    history = client.operation_history(label=f'{user_id}')

    for operation in history.operations:

        if operation.status == 'success' and ((amount_1-(amount_1*0.05)) < operation.amount < amount_1):
            conn = sqlite3.connect('database/USERS.sql')
            cur = conn.cursor()
            cur.execute(f'UPDATE user_{user_id} SET id = "{user_id}"')
            cur.execute(f'UPDATE user_{user_id} SET message_cnt = "{1}"')
            conn.commit()
            cur.close()
            conn.close()

            return 1

        if operation.status == 'success' and ((amount_5-(amount_5*0.05)) < operation.amount < amount_5):
            conn = sqlite3.connect('database/USERS.sql')
            cur = conn.cursor()
            cur.execute(f'UPDATE user_{user_id} SET id = "{user_id}"')
            cur.execute(f'UPDATE user_{user_id} SET message_cnt = "{5}"')
            conn.commit()
            cur.close()
            conn.close()

            return 5

        if operation.status == 'success' and ((amount_10-(amount_10*0.05)) < operation.amount < amount_10):
            conn = sqlite3.connect('database/USERS.sql')
            cur = conn.cursor()
            cur.execute(f'UPDATE user_{user_id} SET id = "{user_id}"')
            cur.execute(f'UPDATE user_{user_id} SET message_cnt = "{10}"')
            conn.commit()
            cur.close()
            conn.close()

            return 10

        if operation.status == 'success' and ((amount_50-(amount_50*0.05)) < operation.amount < amount_50):
            conn = sqlite3.connect('database/USERS.sql')
            cur = conn.cursor()
            cur.execute(f'UPDATE user_{user_id} SET id = "{user_id}"')
            cur.execute(f'UPDATE user_{user_id} SET message_cnt = "{50}"')
            conn.commit()
            cur.close()
            conn.close()

            return 50

    else:
        return False


def check_data_cnt_message(message):
    logging.info('check_data_cnt_message')
    user_id = message.from_user.id
    # ПРОВЕРКА ПОДПИСКИ
    conn = sqlite3.connect('database/USERS.sql')
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM user_{user_id}')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


def check_message_cht(user_id):
    logging.info('check_message_cht')
    # ПОВТОРНАЯ ПРОВЕРКА ПОДПИСКА
    conn = sqlite3.connect('database/USERS.sql')
    cur = conn.cursor()
    cur.execute(f'SELECT message_cnt FROM user_{user_id}')
    cnt = cur.fetchall()
    cur.close()
    conn.close()
    return cnt


def send_message_to_chat(message_to_send, user_id):
    logging.info('send_message_to_chat')
    conn = sqlite3.connect('database/BAD_WORDS.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM bad_words')
    words = cur.fetchall()
    cur.close()
    conn.close()
    # ПРОВЕРКА НА СТОП СЛОВА
    for word_in_list in words:
        word = word_in_list[0]
        if str(word).lower() in message_to_send.lower():
            return False

    else:
        return True

def del_one_message(user_id):
    conn = sqlite3.connect('database/USERS.sql')
    cur = conn.cursor()
    cur.execute(f'SELECT message_cnt FROM user_{user_id}')
    data = cur.fetchall()
    cnt = data[0][0] - 1
    cur.execute(f'UPDATE user_{user_id} SET message_cnt = "{cnt}"')
    conn.commit()
    cur.close()
    conn.close()


def get_chat_id(user_id):
    conn = sqlite3.connect('database/USERS.sql')
    cur = conn.cursor()
    cur.execute(f'SELECT chats_id FROM user_{user_id}')
    id_ = cur.fetchall()
    cur.close()
    conn.close()
    return id_[0][0]


def save_message_to_send(message_to_send,user_id):
    conn = sqlite3.connect('database/USERS.sql')
    cur = conn.cursor()
    cur.execute(f'UPDATE user_{user_id} SET message_to_send = "{message_to_send}"')
    conn.commit()
    cur.close()
    conn.close()

def get_message_to_send(user_id):
    conn = sqlite3.connect('database/USERS.sql')
    cur = conn.cursor()
    cur.execute(f'SELECT message_to_send FROM user_{user_id}')
    message = cur.fetchall()
    cur.close()
    conn.close()
    return message

def get_media(user_id):
    conn = sqlite3.connect('database/USERS.sql')
    cur = conn.cursor()
    cur.execute(f'SELECT media_files FROM user_{user_id}')
    data = cur.fetchall()
    rezult = data[0][0]
    cur.close()
    conn.close()
    return rezult

def update_media_files(user_id,new_media):
    conn = sqlite3.connect('database/USERS.sql')
    cur = conn.cursor()
    cur.execute(f'UPDATE user_{user_id} SET media_files = "{new_media}"')
    conn.commit()
    cur.close()
    conn.close()

def clean_media_files(user_id):
    conn = sqlite3.connect('database/USERS.sql')
    cur = conn.cursor()
    cur.execute(f'UPDATE user_{user_id} SET media_files = "None"')
    conn.commit()
    cur.close()
    conn.close()

def get_group_name_by_id(id):
    conn = sqlite3.connect('database/GROUP_NAME.sql')
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM group_name WHERE id = "{id}"')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


