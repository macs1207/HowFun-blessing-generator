import sqlite3
import os    


def save_to_db(feedback):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    try:
        c.execute('''CREATE TABLE FeedBack(ID INT PRIMARY KEY AUTOINCREMENT, detail varchar(500) NOT NULL);''')
    except:
        print("table exist")
    c.execute(f'''INSERT INTO FeedBack (detail) VALUES({feedback});''')
    conn.commit()
    conn.close()
