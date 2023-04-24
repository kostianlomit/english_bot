import sqlite3

conn = sqlite3.connect('vocabluary.db')
cur = conn.cursor()

cur.execute(f'SELECT * FROM words ORDER BY RANDOM() LIMIT 1')

result = cur.fetchall()
print(result)