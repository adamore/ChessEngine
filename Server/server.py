from flask import Flask 
from flas_restful import Api
import GameManager


app = Flask(__name__)
app = Api(app)

app.add_resource(GameManager, "/make-white-move")

if __name__ == "__main__":
	app.run()