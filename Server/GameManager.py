from flask_restful import Resource, reqparse
from flask import abort
from random import seed
from random import randint
import sys
from threading import Timer
import time

sys.path.insert(0, '../Engine/')
from Game import Game

parser = reqparse.RequestParser()
parser.add_argument("game_id", required=True)
parser.add_argument("move", required=True)
games = dict()

class GameManager(Resource):
    def get(self):
        args = parser.parse_args()
        game_id = int(args["game_id"])
        if game_id not in games:
            abort(404)
        else:
            #Enter time taken move for managing games that are done/not being used
            games[game_id][1] = time.perf_counter()
            #Get game obj
            reqGame = games[game_id][0]
            moveMade = args["move"]
            reqGame.takeTurn(moveMade)
            engineBestMove = reqGame.engineTakeTurn()
            return {"game_id": game_id, "move": engineBestMove}

class GameCreator(Resource):
    def get(self):
        val = None
        while not val or val in games:
            val = randint(0, 10**5)
        games[val] = [Game(), time.perf_counter()]
        return {"game_id": val}

class RepeatedTimer:
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

def manageGameMemory():
    inactiveGames = []
    for gameID in games:
        lastPlayedTime = games[gameID][1]
        if time.perf_counter() - lastPlayedTime >= 10:
            inactiveGames.append(gameID)
    numInactive = len(inactiveGames)
    beforeDeletion = len(games)
    for inactiveID in inactiveGames:
        del games[inactiveID]

MemoryManager = RepeatedTimer(10.0, manageGameMemory)
