"""
data.py
    -handles persistent data storage for resources in the foodlog app
"""

import sqlite3 as db
import os

from foodlog.common.build_db import build_db
from foodlog.common.constants import DB_NAME
from foodlog.common.err import DuplicateRecordError, FoodRecNotFoundError, GroupNotFoundError

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#FOOD REC API


def add_food(food_rec):
    '''
    adds a new food record to the database:
        1. check if food already in db
            if so, abort the request
        2. check if catagory specified exists
            if not, create it
        3. insert the food record
        4. insert food_type link to specified group
    '''
    conn = cnct()
    c = conn.cursor()
    #if food is found, dupe rec error is raised, else continue normally.
    try:
        get_food(food_rec['name'])
        raise DuplicateRecordError
    except FoodRecNotFoundError:
        pass
    #if group isnt found, add it
    try:
        get_group(food_rec['group'])
    except GroupNotFoundError:
        add_group(food_rec['group'])
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
    c.execute('''
              INSERT INTO food_type
              VALUES (?, ?)
              ''', (food_rec['group'], food_rec['name'],))
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
    if food_rec is None:
        raise FoodRecNotFoundError
    else:
        c.execute('''
                  SELECT type_name FROM food_type
                  WHERE food_name = ?
                  ''', (food_name,))
        groups = c.fetchmany()
        food_rec['groups'] = parseTupleList(groups, 'type_name')
        return food_rec


def delete_food(food_name):
    '''
    delete a food_rec if it exists, along w/ all group memberships
    '''
    #throws FoodRecordNotFoundError if the food doesn't exist in the db
    food = get_food(food_name)
    conn = cnct()
    c = conn.cursor()
    c.execute('''
              DELETE FROM food
              WHERE name = ?
              ''', (food_name,))
    c.execute('''
              DELETE FROM food_type
              WHERE food_name = ?
              ''', (food_name,))
    conn.commit()
    return food


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#FOOD GROUP API


def add_group(group_name, group_description=None):
    '''
    insert group into the db if it doesn't exist
    '''
    conn = cnct()
    c = conn.cursor()
    try:
        get_group(group_name)
        raise DuplicateRecordError
    except GroupNotFoundError:
        pass
    if group_description is None:
        group_description = 'No description yet'
    c.execute('''
              INSERT INTO type
              VALUES (?, ?)
              ''', (group_name, group_description,))
    conn.commit()
    return get_group(group_name)


def get_group(group_name):
    '''
    retrieve specified group from the db
    '''
    conn = cnct()
    c = conn.cursor()
    c.execute('''
              SELECT name FROM type
              WHERE name = ?
              ''', (group_name,))
    try:
        group = c.fetchone()
    except Exception:  # there was no group
        raise GroupNotFoundError
    else:
        c.execute('''
                  SELECT food_name FROM food_type
                  WHERE type_name = ?
                  ''', (group_name,))
        foods = c.fetchmany()
        group = {'group': group}
        group['foods'] = parseTupleList(foods, 'food_name')
        return group


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def parseTupleList(tuple_list, column):
    '''
    convert a list of tuples to a list of values associated w/ specified column
    '''
    l = []
    for t in tuple_list:
        l.append(t[column])

    return l


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def cnct():
    '''
    wrapper for database connect routine.
    '''
    if os.path.isfile(DB_NAME):
        conn = db.connect(DB_NAME)
        conn.row_factory = dict_factory
        return conn
    else:
        build_db()
        print "WARNING: the foodlog database did not exist and was re-created"
        return cnct()
