import sqlite3


def get_one_word(message):
    word = message.text

    conn = sqlite3.connect('database/BAD_WORDS.sql')
    cur = conn.cursor()
    cur.execute(f'INSERT INTO bad_words (word) VALUES ("{word}")')
    conn.commit()
    cur.close()
    conn.close()


def get_many_words(message):
    words = str(message.text)
    word_list = words.split(',')

    conn = sqlite3.connect('database/BAD_WORDS.sql')
    cur = conn.cursor()

    for word in word_list:
        cur.execute(f'INSERT INTO bad_words (word) VALUES ("{word}")')
        conn.commit()

    cur.close()
    conn.close()

def create_attach_post(message):
    data = str(message.text)
    data_list = data.split('|')

    return data_list







