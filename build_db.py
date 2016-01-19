import sqlite3 as db

conn = db.connect('foodlog.db')

c = conn.cursor()

c.executer('''
           CREATE TABLE foods
           ()
           ''')
