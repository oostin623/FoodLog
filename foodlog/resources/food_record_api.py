"""
food_record_api.py
    -api for food record resources
"""

from flask import Flask, abort
from flask_restful import Resource, reqparse, fields, marshal


class FoodRecordAPI(Resource):
    """
    """

    #template for marshaling responses to food record POST and GET requests
    FOOD_FIELDS = {'name': fields.String,
                   'catagory': fields.String,
                   'description': fields.String,
                   'price': fields.Float,
                   'calories': fields.Float,
                   'fat': fields.Float,
                   'carbs': fields.Float,
                   'protein': fields.Float,
                   'added_sugar': fields.Float,
                   'fiber': fields.Float}

    def __init__(self):
        """
        init argparser to confirm incoming POST requests are valid
        """
        # note: name and catagory come from url, np need to parse them here
        self.reqparse = reqparse.RequestParser()
        self.reqparse.app_argument('description', type=str, location='json', required=False)
        self.reqparse.app_argument('price', type=str, location='json', required=False)
        self.reqparse.app_argument('calories', type=float, location='json', required=True)
        self.reqparse.app_argument('fat', type=float, location='json', required=True)
        self.reqparse.app_argument('carbs' type=float, location='json', required=True)
        self.reqparse.app_argument('protein' type=float, location='json', required=True)
        self.reqparse.app_argument('added sugar' type=float, location='json', required=True)
        self.reqparse.app_argument('fiber', type=float, location='json', required=False)
        super(FoodRecordAPI, self).__init__()

    def post(self, food_type, food_name):
        """
        POST /foodlog/food-dict/<food_catagory>/<food_name>
            -adds a new food records to the food dictionary
        """
        # parse incoming JSON into a dict
        food_rec = self.reqparse.parse_args()

        try:
            return {'food_rec': marshal(food_rec, self.FOOD_FIELDS)}, 201

        except:
            pass

    def get(self):
        """
        GET /foodlog/food-dict/<food_catagory>/<food_name>
            -retrieves an individual food record by name
        """
        pass

    def put(self):
        """
        *NOT YET IMPLEMENTED*
        """
        pass

    def delete(self):
        """
        *NOT YET IMPLEMENTED*
        """
        pass
