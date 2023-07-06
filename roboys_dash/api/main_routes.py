from flask import Flask
from flask import Blueprint

from flask_restful import Api, Resource

home_bp = Blueprint("api_home", __name__)
home_api = Api(home_bp, errors=Flask.errorhandler)

class HomeAPI(Resource):
    def get(self):
        return {"message": "Hello, World!"}

home_api.add_resource(HomeAPI, "/")
