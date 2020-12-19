from flask_restful import Resource, reqparse, Abort
from random import seed
from random import randint
import sys
sys.path.insert(0, '../Engine/')
import Smiley

parser = reqparse.RequestParser()
games = dict()

class GameManager(Resource):

	def get(self):
		args = parser.parse_args()
		game_id = args["game_id"]
		if game_id not in games:
			abort(404, message = "Game id {} could not be found.".format(game_id))
		else:
			reqGame = games[game_id]

class GameCreator(Resource):
	def get(self):
		val = None
		while not val or val in games:
			val = randint(0,10**5)
		games[val] = MoveTree()
		return {"game_id" : val}



