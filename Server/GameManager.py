from flask_restful import Resource, reqparse
from flask import abort
from random import seed
from random import randint
import sys
sys.path.insert(0, '../Engine/')
from Game import Game

parser = reqparse.RequestParser()
parser.add_argument("game_id", required = True)
parser.add_argument("move",required = True)
games = dict()

class GameManager(Resource):
	def get(self):
		args = parser.parse_args()
		game_id = int(args["game_id"])
		if game_id not in games:
			abort(404)
		else:
			reqGame = games[game_id]
			moveMade = args["move"]
			reqGame.takeTurn(moveMade)
			engineBestMove = reqGame.engineTakeTurn()
			return {
					"game_id" : game_id,
					"move":engineBestMove

			}

class GameCreator(Resource):
	def get(self):
		val = None
		while not val or val in games:
			val = randint(0,10**5)
		games[val] = Game()
		return {"game_id" : val}



