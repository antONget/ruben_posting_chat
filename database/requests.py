import sqlite3
from yoomoney import Client
import logging

def create_table(message):
    logging.info('create_table')
    #СОЗДАНИЕ БД ЕСЛИ ОНИ ЕЩЕ НЕ СОЗДАНЫ
    user_id = message.from_user.id

    conn = sqlite3.connect('database/BAD_WORDS.sql')
    cur = conn.cursor()
    cur.execute(f'CREATE TABLE IF NOT EXISTS bad_words (word text)')
    conn.commit()
    cur.close()
    conn.close()

    conn = sqlite3.connect('database/USERS.sql')
    cur = conn.cursor()
    cur.execute(f'CREATE TABLE IF NOT EXISTS user_{user_id} (id int,message_cnt int)')
    conn.commit()
    cur.close()
    conn.close()


#ДОБАВЛЕНИЕ СТОП-СЛОВ
def get_one_word(message):
    logging.info('get_one_word')
    word = message.text
    #ОДНО СЛОВО
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
    #НЕСКОЛЬКО СЛОВ
    conn = sqlite3.connect('database/BAD_WORDS.sql')
    cur = conn.cursor()

    for word in word_list:
        cur.execute(f'INSERT INTO bad_words (word) VALUES ("{word}")')
        conn.commit()

    cur.close()
    conn.close()


def delete_one_word(message):
    logging.info('delete_one_word')
    user_id =  message.from_user.id
    #ВЫЧИТАНИЕ ОДНОГО СЛОВА ИЗ ЛИМТА СООБЩЕНИЙ ПРИ ОТПРАВКЕ СООБЩЕНИИЯ
    conn = sqlite3.connect('database/USERS.sql')
    cur = conn.cursor()
    cur.execute(f'SELECT message_cnt FROM user_{user_id}')
    data = cur.fetchall()
    cnt = data[0][0] - 1
    cur.execute(f'UPDATE user_{user_id} SET message_cnt = "{cnt}"')
    conn.commit()
    cur.close()
    conn.close()


#ПРОВЕРКА ОПЛАТЫ И ЗАПИСЬ В БД КОЛ-ВА СЛОВ (ПО ПОДПИСКЕ)
def proverka(message, token,amount_15,amount_50,amount_100,amount_200):
    logging.info('proverka')
    PAYMENT_TOKEN = token
    print(PAYMENT_TOKEN)

    user_id = message.from_user.id

    client = Client(PAYMENT_TOKEN)
    history = client.operation_history(label=f'{user_id}')

    for operation in history.operations:

        if operation.status == 'success' and operation.amount == float(amount_15 - (amount_15 * 0.03)):
            conn = sqlite3.connect('database/USERS.sql')
            cur = conn.cursor()
            cur.execute(f'INSERT INTO user_{user_id} (id,message_cnt) VALUES ("{user_id}","{15}")')
            conn.commit()
            cur.close()
            conn.close()

            return 15

        if operation.status == 'success' and operation.amount == float(amount_50 - (amount_50 * 0.03)):
            conn = sqlite3.connect('database/USERS.sql')
            cur = conn.cursor()
            cur.execute(f'INSERT INTO user_{user_id} (id,message_cnt) VALUES ("{user_id}","{50}")')
            conn.commit()
            cur.close()
            conn.close()

            return 50

        if operation.status == 'success' and operation.amount == float(amount_100 - (amount_100 * 0.03)):
            conn = sqlite3.connect('database/USERS.sql')
            cur = conn.cursor()
            cur.execute(f'INSERT INTO user_{user_id} (id,message_cnt) VALUES ("{user_id}","{100}")')
            conn.commit()
            cur.close()
            conn.close()

            return 100

        if operation.status == 'success' and operation.amount == float(amount_200 - (amount_200 * 0.03)):
            conn = sqlite3.connect('database/USERS.sql')
            cur = conn.cursor()
            cur.execute(f'INSERT INTO user_{user_id} (id,message_cnt) VALUES ("{user_id}","{200}")')
            conn.commit()
            cur.close()
            conn.close()

            return 200

    else:
        return False


def check_data_cnt_message(message):
    logging.info('check_data_cnt_message')
    user_id = message.from_user.id
    #ПРОВЕРКА ПОДПИСКИ
    conn = sqlite3.connect('database/USERS.sql')
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM user_{user_id}')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


def check_message_cht(user_id):
    logging.info('check_message_cht')
    #ПОВТОРНАЯ ПРОВЕРКА ПОДПИСКА
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
    #ПРОВЕРКА НА СТОП СЛОВА
    for word_in_list in words:
        word = word_in_list[0]
        if str(word).lower() in message_to_send.lower():
            return False

    else:
        conn = sqlite3.connect('database/USERS.sql')
        cur = conn.cursor()
        cur.execute(f'SELECT message_cnt FROM user_{user_id}')
        data = cur.fetchall()
        cnt = data[0][0] - 1
        cur.execute(f'UPDATE user_{user_id} SET message_cnt = "{cnt}"')
        conn.commit()
        cur.close()
        conn.close()

        return True
