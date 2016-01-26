"""
build_db.py 

    -builds the foodlog databases if they do not exist

    1. build catagory table
    2. build food table
    3. build log_entry table

"""

import sqlite3 as db

conn = db.connect('foodlog.db')
c = conn.cursor()

table1 = catagory
table2 = food
table3 = log_entry

c.execute('''
          CREATE TABLE IF NOT EXISTS {t1}
          (name TEXT PRIMARY KEY NOT NULL,
           description TEXT NOT NULL)
          '''.format(t1=table1))

c.execute('''
           CREATE TABLE IF NOT EXISTS {t2}
           (name TEXT  PRIMARY KEY NOT NULL,
            FOREIGN KEY (catagory) REFRENCES,
            description TEXT,
            price REAL,
            calories REAL NOT NULL, fat real, carbs real, protein real,
            added_sugar real, fiber real)
           '''.format(t2=table2))

c.execute('''
          CREATE TABLE IF NOT EXISTS {t3}
          (date
           time
           food_name
           servings


           meal)
          ''')
