import sqlite3
import os    

path = os.getcwd()

def conn_database(feedback):

    conn = sqlite3.connect(path + "\\feedback.db")
    c = conn.cursor()
    try:
        c.execute('''CREATE TABLE FeedBack(ID INT PRIMARY KEY   AUTOINCREMENT, detail varchar(500) NOT NULL);''')
    except:
        print("table exist")
    c.execute('''INSERT INTO FeedBack (detail) VALUES(\"%s\");'''%(feedback))
    conn.commit()
    conn.close()
    return feedback
if __name__ == "__main__":
    print(conn_database("test"))