from flask import Flask 
from flask_restful import Api
import GameManager


app = Flask(__name__)
app = Api(app)

app.add_resource(GameManager, "/make-white-move")
app.add_resource(GameCreator, "/create-game")


if __name__ == "__main__":
	app.run()