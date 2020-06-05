from sqlite3 import OperationalError
import sqlite3
import os


def save_to_db(feedback):
    conn = sqlite3.connect("howfun.db")
    c = conn.cursor()
    try:
        c.execute('''CREATE TABLE feedback(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            detail varchar(500) NOT NULL
        );''')
    except OperationalError as e:
        print("table exist")

    c.execute(f'''INSERT INTO feedback (detail) VALUES ("{feedback}");''')
    conn.commit()
    conn.close()
