import Smiley
import chess

class Game:
	def __init__(self):
		self.Engine = Smiley.MoveTree()
		self.board = chess.Board()
		self.USER_COLOR = chess.WHITE
		self.ENGINE_COLOR = chess.BLACK

	def takeTurn(self, alg):
		self.Engine.takeTurn(alg)
		self.board.push(chess.Move.from_uci(alg))
		return

	def engineTakeTurn(self):
		#Let engine find best move
		bestMove = self.Engine.findBestMove()
		#Convert move to uci algebraic format
		bestMoveUCI = bestMove.uci()
		self.takeTurn(bestMoveUCI)
		return bestMoveUCI






