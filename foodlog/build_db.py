"""
build_db.py

    -builds the foodlog databases if they do not exist

"""

import sqlite3 as db

from foodlog.common.constants import DB_NAME


def build_db():
    conn = db.connect(DB_NAME)
    c = conn.cursor()

    table1 = 'type'
    table2 = 'food'
    table3 = 'food_type'
    table4 = 'log'

    #build food catagory table
    c.execute('''
              CREATE TABLE IF NOT EXISTS {t1}
              (name TEXT PRIMARY KEY NOT NULL,
               description TEXT NOT NULL)
              '''.format(t1=table1))

    #build food record table
    c.execute('''
               CREATE TABLE IF NOT EXISTS {t2}
               (name TEXT  PRIMARY KEY NOT NULL,
                {t1}_name TEXT,
                description TEXT,
                price REAL,
                calories REAL NOT NULL,
                fat REAL NOT NULL,
                carbs REAL NOT NULL,
                protein REAL NOT NULL,
                added_sugar REAL,
                fiber REAL,
                FOREIGN KEY ({t1}_name) REFERENCES {t1}(name))
                '''.format(t2=table2, t1=table1))

    #build food_groups table
    c.execute('''
              CREATE TABLE IF NOT EXISTS {t3}
              ({t1}_name TEXT,
               {t2}_name TEXT,
               FOREIGN KEY ({t1}_name) REFERENCES {t1}(name),
               FOREIGN KEY ({t2}_name) REFERENCES {t2}(name))
              '''.format(t1=table1, t2=table2, t3=table3))

    #build log record table
    c.execute('''
              CREATE TABLE IF NOT EXISTS {t4}
              (time DATETIME NOT NULL,
               {t2}_name TEXT,
               servings REAL NOT NULL,
               meal TEXT,
               FOREIGN KEY ({t2}_name) REFERENCES {t2}(name))
              '''.format(t4=table4, t2=table2))

    conn.commit()
    conn.close()


if __name__ == '__main__':
    build_db()
