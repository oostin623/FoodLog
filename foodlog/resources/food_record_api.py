"""
food_record_api.py
    -api for food record resources
"""

from flask import abort
from flask_restful import Resource, reqparse, fields, marshal

from foodlog.common import data


class FoodRecordAPI(Resource):
    """
    -api for interaction with food dictionary on an individual record
        GET  -examine a food record (+ all associated groups)
        POST  -add a food record (+new group if the group specified doesn't exist)
    """

    #template for marshaling responses to food record POST and GET requests
    #note: groups is a list of 1 or more food groups
    FOOD_FIELDS = {'name': fields.String,
                   'description': fields.String,
                   'groups': fields.List(fields.String),
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
        # note: name and catagory come from url, no need to parse them here
        self.reqparse = reqparse.RequestParser()
        self.reqparse.app_argument('description', type=str, location='json', required=False)
        self.reqparse.app_argument('price', type=str, location='json', required=False)
        self.reqparse.app_argument('calories', type=float, location='json', required=True)
        self.reqparse.app_argument('fat', type=float, location='json', required=True)
        self.reqparse.app_argument('carbs', type=float, location='json', required=True)
        self.reqparse.app_argument('protein', type=float, location='json', required=True)
        self.reqparse.app_argument('added sugar', type=float, location='json', required=True)
        self.reqparse.app_argument('fiber', type=float, location='json', required=False)
        super(FoodRecordAPI, self).__init__()

    def post(self, food_group, food_name):
        """
        POST /foodlog/food-dict/<food_name>
            -adds a new food records to the food dictionary
        """
        # parse incoming JSON into a dict
        food_rec = self.reqparse.parse_args()
        # add the food_type and food_name from the url
        food_rec['name'] = food_name
        food_rec['group'] = food_group
        # add the new food record to the database
        try:
            data.add_food(food_rec)
            return {'food_rec': marshal(food_rec, self.FOOD_FIELDS)}, 201
        except Exception:
            abort("An error has occured.")

    def get(self):
        """
        GET /foodlog/food-dict/<food_name>
            -retrieves an individual food record by name, 
             along with a list of groups the food is in
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
