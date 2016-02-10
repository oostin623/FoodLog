"""
data.py
    -handles persistent data storage for resources in the foodlog app
"""

import sqlite3 as db
import os

from FoodLog.build_db import build_db
from foodlog.common.constants import DB_NAME
from foodlog.common.err import DuplicateRecordError


def add_food(food_rec):
    '''
        -adds a new food record to the database.
            1. check if food already in db
                if so, abort the request
            2. check if catagory specified exists
                if not, create it
            3. insert the food record w/ foreign key ref to the catagory
    '''
    conn = cnct()
    c = conn.cursor()
    # check for duplicate food name
    if get_food(food_rec['name']) is not None:
        raise DuplicateRecordError
    # check if category exists
    elif get_catagory(food_rec['catagory']) is None:
        add_catagory(food_rec['catagory'])
    # insert food
    c.execute('''
              INSERT INTO food
              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
              ''',
              food_rec['name'],
              food_rec['description'],
              food_rec['price'],
              food_rec['calories'],
              food_rec['fat'],
              food_rec['carbs'],
              food_rec['protein'],
              food_rec['added_sugar'],
              food_rec['fiber'])
    # insert group
    c.execute('''
              INSERT INTO food_group
              VALUES (?, ?)
              ''', food_rec['name'], food_rec['group'])
    conn.commit()


def get_food(food_name):
    '''
        -retrieves food_rec attrubutes associated w/ specified food_name
            note: does not retrieve food_group info
    '''
    conn = cnct()
    c = conn.cursor()

    c.execute('''
              SELECT * FROM food
              WHERE name = ?
              '''
              )

def get_foods_groups(food_name):
    '''
    '''


    pass


def get_catagory(c, catagory):
    c.execute('''
              SELECT name FROM catagory
              WHERE name = ?
              ''', catagory)
    return c.fetchone()


def add_catagory():
    pass


def cnct():
    '''
    wrapper for database connect routine.
    '''
    if os.path.isfile(DB_NAME):
        conn = db.connect('foodlog.db')
        return conn
    else:
        build_db()
        print "WARNING: db did not exist and was re-created"
        return cnct()
