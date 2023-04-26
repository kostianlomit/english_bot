#создаем базу Vocabluary

import sqlite3

conn = sqlite3.connect('vocabluary.db')
cur = conn.cursor()

cur.execute('CREATE TABLE words(user_id INTEGER, word TEXT, definition TEXT)')
