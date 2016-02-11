"""
data.py
    -handles persistent data storage for resources in the foodlog app
"""

import sqlite3 as db
import os

from foodlog.build_db import build_db
from foodlog.common.constants import DB_NAME
from foodlog.common.err import DuplicateRecordError, FoodRecNotFoundError

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#FOOD REC API


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

    # check if group exists
    elif get_group(food_rec['group']) is None:
        add_group(food_rec['group'])

    # insert food
    c.execute('''
              INSERT INTO food
              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
              ''',
              (food_rec['name'],
              food_rec['description'],
              food_rec['price'],
              food_rec['calories'],
              food_rec['fat'],
              food_rec['carbs'],
              food_rec['protein'],
              food_rec['added sugar'],
              food_rec['fiber'],))

    # insert food group linking
    c.execute('''
              INSERT INTO food_type
              VALUES (?, ?)
              ''', (food_rec['name'], food_rec['group'],))
    conn.commit()

    return get_food(food_rec['name'])


def get_food(food_name):
    '''
    -retrieves food_rec attrubutes associated w/ specified food_name,
     also gets a list of groups the food is a member of
    '''
    conn = cnct()
    c = conn.cursor()

    c.execute('''
              SELECT * FROM food
              WHERE name = ?
              ''', (food_name,))

    food_rec = c.fetchone()

    if food_rec is not None:
        c.execute('''
                  SELECT type_name FROM food_type
                  WHERE food_name = ?
                  ''', (food_name,))
        #add the list of groups
        food_rec['groups'] = c.fetchmany()

    return food_rec


def delete_food(food_name):
    '''
    -delete a food_rec if it exists,
     along w/ all group memberships
    '''
    conn = cnct()
    c = conn.cursor()

    c.execute('''
              SELECT * FROM food
              WHERE name = ?
              ''', food_name)
    food = c.fetchone()

    #if food nto found abort the request
    if food is None:
        raise FoodRecNotFoundError
    else:
        c.execute('''
                  DELETE FROM food
                  WHERE name = ?
                  ''', food_name)
        c.execute('''
                  DELETE FROM food_type
                  WHERE food_name = ?
                  ''', food_name)
        c.commit()

        #return info for the deleted food
        return get_food(food_name)


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#FOOD GROUP API


def add_group(group_name, group_description=None):
    '''
    '''
    conn = cnct()
    c = conn.cursor()

    #confirms group doesn't already exist
    if get_group(group_name) is not None:
        raise DuplicateRecordError

    if group_description is None:
        group_description = 'No description yet'

    c.execute('''
              INSERT INTO type
              VALUES (?, ?)
              ''', (group_name, group_description,))

    group = {"name": group_name, "description": group_description}
    return group


def get_group(group_name):
    '''
    '''
    conn = cnct()
    c = conn.cursor()

    c.execute('''
              SELECT name FROM type
              WHERE name = ?
              ''', (group_name,))

    return c.fetchone()


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
