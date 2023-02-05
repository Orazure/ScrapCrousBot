from conDb import *
import sqlite3

conn=create_connection(r"G:\Dev\CrousBot\CrousBotScrap\db\datas.sqlite3")

conn.execute('''CREATE TABLE months
         (ID INT PRIMARY KEY     NOT NULL,
         day           TEXT    NOT NULL,
         number_of_dishes INT NOT NULL,
         status INT,
         dishes TEXT NOT NULL);''')

print("Table created successfully")

conn.close()