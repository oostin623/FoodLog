"""
app.py
    -exposes 2 APIs for food dictionary and food record resources
"""

from flask import Flask
from flask_restful import Api

from foodlog.resources.food_record_api import FoodRecordAPI
#from foodlog.resources.food_dict_api import FoodDictAPI

# instanciate a flask_restful RESTful API app
APP = Flask(__name__)
API = Api(APP)

# add resources w/ associated url routes and endpoints
API.add_resource(FoodRecordAPI,
                 '/foodlog/food-dict/<string:food_name>',
                 endpoint='food_rec')

#API.add_resource(FoodDictAPI,
#                 '/foodlog/food-dict/<string:food_group>',
#                 endpoint='food_dict')

# run the web service in debug mode if this script is executed manually
if __name__ == '__main__':
    APP.run(debug=True)
