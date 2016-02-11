"""
food_group_api.py
    -api for food the group resource collection (list of food groups)
"""

from flask import Flask, abort
from flask_restful import Resource, reqparse, fields, marshal


class FoodGroupAPI(Resource):
    #add requestparser

    def get(self):
        """
        GET /foodlog/food-dict/groups/<food_group>
        """
        pass

    def delete(self):
        """
        DELETE /foodlog/food-dict/groups/
        """
        pass
