import sqlite3


def get_one_word(message):
    word = message.text

    conn = sqlite3.connect('database/BAD_WORDS.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM bad_words')
    data = cur.fetchall()
    for elem in data:
        if word == elem[0]:
            break
    else:
        cur.execute(f'INSERT INTO bad_words (word) VALUES ("{word}")')
    conn.commit()
    cur.close()
    conn.close()


def get_many_words(message):
    words = str(message.text)
    word_list = words.split(',')

    conn = sqlite3.connect('database/BAD_WORDS.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM bad_words')
    data = cur.fetchall()
    for word in word_list:
        for elem in data:
            if word == elem[0]:
                print(elem[0],word)
                break
        else:
            cur.execute(f'INSERT INTO bad_words (word) VALUES ("{word}")')
            conn.commit()
    cur.close()
    conn.close()


def create_attach_post(message):
    data = str(message.text)
    data_list = data.split('|')

    return data_list


def get_all_stop_words():
    conn = sqlite3.connect('database/BAD_WORDS.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM bad_words')
    data = cur.fetchall()
    cur.close()
    conn.close()
    if data:
        words = ''
        for elem in data:
            word = str(elem[0]) + ','
            words += word
        return words
    else:
        return 'Список стоп-слов пуст'


def delete_all_stop_words():
    conn = sqlite3.connect('database/BAD_WORDS.sql')
    cur = conn.cursor()
    cur.execute('DELETE FROM bad_words')
    conn.commit()
    cur.close()
    conn.close()
    return True
