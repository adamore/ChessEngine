import chess
from pptree import *
import numpy as np


PIECE_VALUES = {
	chess.PAWN: 1,
	chess.KNIGHT: 3,
	chess.BISHOP: 3,
	chess.ROOK: 5,
	chess.QUEEN: 9
}

class MoveNode:
	def __init__(self, move, val, prev, color):
		self.move = move
		self.val = val
		self.parent = prev
		self.nxt = dict()
		self.children = []
		self.searchable = True
		self.optimalMove = None
		self.color = color
		if self.parent:
			self.depth = self.parent.depth + 1
			self.color = not self.parent.color
		else:
			self.depth = 0

	def __str__(self):
		return str(self.val)
	def addNextMove(self, nxt):
		self.nxt.append(nxt)
	def getNxtMoves(self):
		return self.nxt

	def getMinFromChildren(self):
		childMin = np.inf
		minNodeMove = None
		for move in self.nxt:
			if self.nxt[move].val != None and self.nxt[move].val < childMin:
				childMin = self.nxt[move].val
				minNodeMove = move
		return minNodeMove

	def getMaxFromChildren(self):
		childMax = -np.inf
		maxNodeMove = None
		for move in self.nxt:
			if self.nxt[move].val != None  and self.nxt[move].val > childMax:
				childMax = self.nxt[move].val
				maxNodeMove = move
		return maxNodeMove

	def setValueBasedOnChildren(self):
		if len(self.nxt) > 0:
			if self.color == chess.WHITE:
				self.optimalMove = self.getMaxFromChildren()
			else:
				self.optimalMove = self.getMinFromChildren()
			self.val = self.nxt[self.optimalMove].val







class MoveTree:
	def __init__(self):
		self.root = None
		self.color = chess.WHITE
		self.turn = chess.WHITE
		self.MAX_SEARCH_DEPTH = 4
		self.board = chess.Board()


	def printTree(self):
		print_tree(self.root, "children")

		
	def evaluateBoardScore(self):
		white_pawns = len(self.board.pieces(chess.PAWN, chess.WHITE)) * PIECE_VALUES[chess.PAWN]
		white_knights = len(self.board.pieces(chess.KNIGHT, chess.WHITE)) * PIECE_VALUES[chess.KNIGHT]
		white_bishops = len(self.board.pieces(chess.BISHOP, chess.WHITE)) * PIECE_VALUES[chess.BISHOP]
		white_rooks = len(self.board.pieces(chess.ROOK, chess.WHITE)) * PIECE_VALUES[chess.ROOK]
		white_queen = len(self.board.pieces(chess.QUEEN, chess.WHITE)) * PIECE_VALUES[chess.QUEEN]
		white_value = white_pawns + white_knights + white_bishops + white_rooks + white_queen

		black_pawns = len(self.board.pieces(chess.PAWN, chess.BLACK)) * PIECE_VALUES[chess.PAWN]
		black_knights = len(self.board.pieces(chess.KNIGHT, chess.BLACK)) * PIECE_VALUES[chess.KNIGHT]
		black_bishops = len(self.board.pieces(chess.BISHOP, chess.BLACK)) * PIECE_VALUES[chess.BISHOP]
		black_rooks = len(self.board.pieces(chess.ROOK, chess.BLACK)) * PIECE_VALUES[chess.ROOK]
		black_queen = len(self.board.pieces(chess.QUEEN, chess.BLACK)) * PIECE_VALUES[chess.QUEEN]
		black_value = black_pawns + black_knights + black_bishops + black_rooks + black_queen
		
		return white_value - black_value 

	def constructTree(self):
		self.root = MoveNode("Root", 0, None, self.color)
		init_moves = self.board.legal_moves
		for move in init_moves:
			self.board.push(move)
			nextNode = MoveNode(move.uci(), self.evaluateBoardScore(), self.root, not self.turn)
			self.root.nxt[move.uci()] = nextNode
			self.root.children.append(nextNode)
			self.board.pop()
	def evaluateDownPath(self, node):
		currNode = node
		if node.depth - self.root.depth <= self.MAX_SEARCH_DEPTH:
			if len(node.nxt) == 0:
				possible_moves = self.board.legal_moves
				for move in possible_moves:
					self.board.push(move)
					nxtNode = MoveNode(move.uci(), self.evaluateBoardScore(), currNode, not currNode.color)
					self.evaluateDownPath(nxtNode)
					currNode.nxt[move.uci()] = nxtNode
					currNode.children.append(nxtNode)
					self.board.pop()
			else:
				for nxtMove in node.nxt:
					self.board.push(chess.Move.from_uci(node.nxt[nxtMove].move))
					self.evaluateDownPath(node.nxt[nxtMove])
					self.board.pop()
	
	def searchTreeForMove(self, node):
		if len(node.nxt) < 1:
			return node.val
		else:
			for move in node.nxt:
				self.searchTreeForMove(node.nxt[move])
				node.nxt[move].setValueBasedOnChildren()
			node.setValueBasedOnChildren()


			
	def makeMoveOnBoard(self, move):
		self.board.push(move)
		self.turn = not self.turn
		if move.uci() in self.root.nxt:
			self.root = self.root.nxt[move.uci()]
		else:
			self.constructTree()






class Engine:
	def __init__(self):
		self.board = chess.Board()
		self.color = chess.BLACK
		self.SEARCH_DEPTH = 0


	def getBoard(self):
		return self.board

	def evaluateBoardScore(self):

		white_pawns = len(self.board.pieces(chess.PAWN, chess.WHITE)) * PIECE_VALUES[chess.PAWN]
		white_knights = len(self.board.pieces(chess.KNIGHT, chess.WHITE)) * PIECE_VALUES[chess.KNIGHT]
		white_bishops = len(self.board.pieces(chess.BISHOP, chess.WHITE)) * PIECE_VALUES[chess.BISHOP]
		white_rooks = len(self.board.pieces(chess.ROOK, chess.WHITE)) * PIECE_VALUES[chess.ROOK]
		white_queen = len(self.board.pieces(chess.QUEEN, chess.WHITE)) * PIECE_VALUES[chess.QUEEN]
		white_value = white_pawns + white_knights + white_bishops + white_rooks + white_queen

		black_pawns = len(self.board.pieces(chess.PAWN, chess.BLACK)) * PIECE_VALUES[chess.PAWN]
		black_knights = len(self.board.pieces(chess.KNIGHT, chess.BLACK)) * PIECE_VALUES[chess.KNIGHT]
		black_bishops = len(self.board.pieces(chess.BISHOP, chess.BLACK)) * PIECE_VALUES[chess.BISHOP]
		black_rooks = len(self.board.pieces(chess.ROOK, chess.BLACK)) * PIECE_VALUES[chess.ROOK]
		black_queen = len(self.board.pieces(chess.QUEEN, chess.BLACK)) * PIECE_VALUES[chess.QUEEN]
		black_value = black_pawns + black_knights + black_bishops + black_rooks + black_queen

		if self.color == chess.BLACK:
			return black_value - white_value
		else:
			return white_value - black_value

	def evalutePotentialMoves(self):
		init_moves = self.board.legal_moves
		move_tree = dict()
		for move in init_moves:
			self.board.push(move)
			move_score = self.evaluateBoardScore()


	def constructMoveTree(self):
		all_legal_moves = self.board.legal_moves
		init_moves = []
		for move in all_legal_moves:
			self.board.push(move)
			move_score = self.evaluateBoardScore()
			init_move_root = MoveNode(move, move_score, None, self.color)
			
			
			nxtLegalMoves = self.board.legal_moves
			turn  = not self.color
			


			init_moves.append(currNode)













ai = MoveTree()
ai.constructTree()
ai.evaluateDownPath(ai.root)
#ai.printTree()
ai.searchTreeForMove(ai.root)
print(ai.root.optimalMove)




