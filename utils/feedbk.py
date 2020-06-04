import sqlite3
import os    

path = os.getcwd()

def conn_database(feedback):

    conn = sqlite3.connect(path + "\\feedback.db")
    c = conn.cursor()
    try:
        c.execute('''CREATE TABLE FeedBack(ID INTEGER PRIMARY KEY   AUTOINCREMENT, detail varchar(500) NOT NULL);''')
    except:
        pass
    c.execute('''INSERT INTO FeedBack (detail) VALUES(\"%s\");'''%(feedback))
    conn.commit()
    conn.close()
