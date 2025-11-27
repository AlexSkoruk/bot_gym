import sqlite3
conn = sqlite3.connect('main.db')
cur = conn.cursor()
cur.execute('DELETE FROM students')
cur.execute('DELETE FROM coaches')
cur.execute('DELETE FROM matches')
conn.commit()
conn.close()
