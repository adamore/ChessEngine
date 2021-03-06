from flask import Flask 
from flask_restful import Api
from GameManager import GameManager, GameCreator

from flask_restful import Resource, reqparse
from flask_cors import CORS, cross_origin
from flask import abort
from random import seed
from random import randint
import sys
sys.path.insert(0, '../Engine/')
import Engine

app = Flask(__name__)
cors = CORS(app)
api = Api(app)

class Homepage(Resource):
	def get(self):
		return {'hello': 'world'}

api.add_resource(Homepage, "/")
api.add_resource(GameManager, "/make-white-move")
api.add_resource(GameCreator, "/create-game")


if __name__ == "__main__":
	app.run(debug=True)