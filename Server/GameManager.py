from flask_restful import Resource, reqparse, Abort

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



