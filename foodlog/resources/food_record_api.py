"""
food_record_api.py
    -api for food record resources
"""

from flask_restful import Resource, reqparse, fields, marshal

from foodlog.common import data
from foodlog.common.err import MyException


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
        # note: name comes from url, no need to parse it here
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('group', type=str, location='json', required=True)
        self.reqparse.add_argument('description', type=str, location='json', required=False)
        self.reqparse.add_argument('price', type=str, location='json', required=False)
        self.reqparse.add_argument('calories', type=float, location='json', required=True)
        self.reqparse.add_argument('fat', type=float, location='json', required=True)
        self.reqparse.add_argument('carbs', type=float, location='json', required=True)
        self.reqparse.add_argument('protein', type=float, location='json', required=True)
        self.reqparse.add_argument('added sugar', type=float, location='json', required=True)
        self.reqparse.add_argument('fiber', type=float, location='json', required=False)
        super(FoodRecordAPI, self).__init__()

    def post(self, food_name):
        """
        POST /foodlog/food-dict/<food_name>
            -adds a new food records to the food dictionary
        """
        # parse incoming JSON into a dict
        food_rec = self.reqparse.parse_args()
        # add the food_name from the url
        food_rec['name'] = food_name
        # add the new food record to the database

        food_rec = data.add_food(food_rec)
        return {'food_rec': marshal(food_rec, self.FOOD_FIELDS)}, 201

    def get(self, food_name):
        """
        GET /foodlog/food-dict/<food_name>
            -retrieves an individual food record by name,
             along with a list of groups the food is in
        """

        food_rec = data.get_food(food_name)
        return {'food_rec': marshal(food_rec, self.FOOD_FIELDS)}, 201

    def delete(self):
        """
        DELETE /foodlog/food-dict/<food_name>
            -delete a food_rec, removing it from all groups
        """

        data.delete_food(food_name)
        return {'food_rec': marshal(food_rec, self.FOOD_FIELDS)}, 201

    def put(self):
        """
        *NOT YET IMPLEMENTED*
        """
        pass
