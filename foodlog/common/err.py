"""
err.py
    -custom exceptions for specific error cases in the foodlog app
"""


class MyException(Exception):
    '''
    custom base exception never thrown, used to catch all custome eceptions
    '''
    pass


class DuplicateRecordError(MyException):
    '''
    thrown if a POST request for a food_rec is made w/ a food_name
    that al;ready exists
    '''
    pass


class FoodRecNotFoundError(MyException):
    '''
    thrown if a GET or DELETE request is made on a food_rec that doesn't exist
    '''
    pass


class GroupNotFoundError(MyException):
    '''
    thrown if a GET or DELETE request is made on a group that doesn't exist
    '''
    pass
