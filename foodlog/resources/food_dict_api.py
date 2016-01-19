"""
food_dict_api.py
    -api for food dictionary resource collection (list of food records)
"""

from flask import Flask, abort
from flask_restful import Resource, reqparse, fields, marshal


class FoodDictionaryAPI(Resource):
    #add requestparser

    def get(self):
        """
        GET /foodlog/food-dict/
        """
        pass

    def delete(self):
        """
        DELETE /foodlog/food-dict/
        """
        pass
