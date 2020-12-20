import sys
sys.path.insert(0, '../chess')

import chess
import numpy as np 
from pptree import *
import chess.polyglot
import pdb
import time

PIECE_VALUES = {
	0: 0,
	chess.PAWN: 1,
	chess.KNIGHT: 3,
	chess.BISHOP: 3,
	chess.ROOK: 5,
	chess.QUEEN: 9,
	chess.KING: 0
}
SQUARE_VALUES  = np.array([
	[ 1, 1, 1, 1, 1, 1, 1, 1],
	[ 1, 1, 1, 1, 1, 1, 1, 1],
	[ 1, 1, 2, 2, 2, 2, 1, 1],
	[ 1, 1, 2, 5, 5, 2, 1, 1],
	[ 1, 1, 2, 5, 5, 2, 1, 1],
	[ 1, 1, 2, 2, 2, 2, 1, 1],
	[ 1, 1, 1, 1, 1, 1, 1, 1],
	[ 1, 1, 1, 1, 1, 1, 1, 1]
])

SQUARES = np.array([
	[chess.A1,chess.B1,chess.C1,chess.D1,chess.E1,chess.F1,chess.G1,chess.H1],
	[chess.A2,chess.B2,chess.C2,chess.D2,chess.E2,chess.F2,chess.G2,chess.H2],
	[chess.A3,chess.B3,chess.C3,chess.D3,chess.E3,chess.F3,chess.G3,chess.H3],
	[chess.A4,chess.B4,chess.C4,chess.D4,chess.E4,chess.F4,chess.G4,chess.H4],
	[chess.A5,chess.B5,chess.C5,chess.D5,chess.E5,chess.F5,chess.G5,chess.H5],
	[chess.A6,chess.B6,chess.C6,chess.D6,chess.E6,chess.F6,chess.G6,chess.H6],
	[chess.A7,chess.B7,chess.C7,chess.D7,chess.E7,chess.F7,chess.G7,chess.H7],
	[chess.A8,chess.B8,chess.C8,chess.D8,chess.E8,chess.F8,chess.G8,chess.H8]
])

class MoveNode:
	def __init__(self, move, parent, fen, color = None):
		self.validNode = True
		#Previous move in chain
		self.parent = parent
		#Set depth of node
		if self.parent:
			self.depth = self.parent.depth + 1
			self.color = not self.parent.color
			if self.color == chess.WHITE:
				self.alpha = -np.inf
				if self.parent.beta != np.inf: 
					self.beta = self.parent.beta
				else:
					self.beta = np.inf
			elif self.color == chess.BLACK:
				self.beta = np.inf
				if self.parent.alpha != -np.inf:
					self.alpha = self.parent.alpha
				else:
					self.alpha = -np.inf

		else:
			self.depth = 0
			self.color = chess.WHITE
			self.score = 0
			self.alpha = -np.inf
			self.beta = np.inf
		#BitBoard representation of previous node
		self.BitBoard = chess.Board(fen)
		#Change BitBoard to current node state
		if move:
			#Make sure this is not representation of root node
			self.BitBoard.push(move)
			#Identify move made at current node
			self.moveUCI = move.uci()
		#Current score of node
		#self.evalutateBoardScore()
		self.score = 0
		#All possible legal move nodes from this state
		self.children = dict()
		#Current optimal node
		self.optimalMove = None
		if self.color == chess.WHITE:
			self.opimalMoveScore = -np.inf
		else:
			self.opimalMoveScore = np.inf
		#The color of whose move is next
		self.debugChildrenList = []



	def __str__(self):
		return self.moveUCI + " " + str(self.score)
	def evalutateBoardScore(self):
		whiteScore = 0
		blackScore = 0
		for i in range(8):
			for j in range(8):
				piece = self.BitBoard.piece_at(SQUARES[i][j])
				if piece and piece.color == chess.WHITE:
					whiteScore += PIECE_VALUES[piece.piece_type] + SQUARE_VALUES[i][j]
				elif piece:
					blackScore += PIECE_VALUES[piece.piece_type] + SQUARE_VALUES[i][j]
		self.score = whiteScore - blackScore
		return self.score

	def propagateAlphaBetaDown(self):
		'''
		if self.color == chess.WHITE:
			if self.parent

		elif self.color == chess.BLACK:
		'''

	def minMaxPropagation(self, ChildScore, NextMove, node):
		if self.color == chess.BLACK:
			if ChildScore < self.opimalMoveScore:
				self.opimalMoveScore = ChildScore
				self.optimalMove = NextMove
				if self.parent:
					self.parent.minMaxPropagation(self.opimalMoveScore, self.moveUCI, self)
		elif self.color == chess.WHITE:
			if ChildScore > self.opimalMoveScore:
				self.opimalMoveScore = ChildScore
				self.optimalMove = NextMove
				if self.parent:
					self.parent.minMaxPropagation(self.opimalMoveScore, self.moveUCI, self)
	'''
	def propagteAlphaBetaUp(self, ChildAlpha, ChildBeta, ChildScore, ChildMove):
		if self.color == chess.WHITE:
			if self.alpha < ChildScore:


		elif self.color == chess.BLACK:
	'''

	def propagateScoreUp(self, ChildScore, NextMove, node):
		if self.color == chess.WHITE:
			if self.alpha < ChildScore:
				self.alpha = ChildScore
			if self.beta < self.alpha:
				if NextMove in self.children:
					self.deleteChild(NextMove)
				else:
					node.validNode = False
		elif self.color == chess.BLACK:
			if self.beta > ChildScore:
				self.beta = ChildScore
			if self.beta < self.alpha:
				if NextMove in self.children:
					print("Deleting")
					self.deleteChild(NextMove)
				else:
					node.validNode = False

		'''
		if self.color == chess.WHITE and ChildScore > self.score:
			self.optimalMove = NextMove
			self.score = ChildScore
			if self.parent:
				self.parent.propagateScoreUp(self.score, self.moveUCI, self)
		elif self.color == chess.BLACK and ChildScore < self.score:
			self.optimalMove = NextMove
			self.score = ChildScore
			if self.parent:
				self.parent.propagateScoreUp(self.score, self.moveUCI, self)
		'''

	def alphaBetaPrune(self):
		return
	def createChildren(self):
		init_moves = self.BitBoard.legal_moves
		for move in init_moves:
			nxtNode = MoveNode(move, self, self.BitBoard.fen())
			if nxtNode.validNode:
				self.children[move.uci()] = nxtNode
				self.debugChildrenList.append(nxtNode)
		#self.getMinOfChildren()
		#self.getMaxOfChildren()
		

	def getMinOfChildren(self):
		childMin = np.inf
		minMoveNode = None
		for childMove in self.children:
			if self.children[childMove].score < childMin:
				childMin = self.children[childMove].score
				minMoveNode = self.children[childMove]
		#self.beta = childMin
		return minMoveNode

	def getMaxOfChildren(self):
		childMax = -np.inf
		maxMoveNode = None
		for childMove in self.children:
			if self.children[childMove].score > childMax:
				childMax = self.children[childMove].score
				maxMoveNode = self.children[childMove]
		#self.alpha = childMax
		return maxMoveNode

	def getMinMaxScore(self):
		if self.color == chess.WHITE:
			maxChildNode = getMaxOfChildren()
			if maxChildNode:
				self.score = maxChildNode.score
				self.optimalMove = maxChildNode
		else:
			minChildNode = getMinOfChildren()
			if minChildNode:
				self.score = minChildNode.score
				self.optimalMove = minChildNode
		return self.score

	def deleteChild(self, move):
		if move in self.children:
			self.debugChildrenList.remove(self.children[move])
			del self.children[move]
			if not self.debugChildrenList and self.parent:
				self.parent.deleteChild(self.moveUCI)

		else:
			return
	def getChild(self, move):
		if move in self.children:
			return self.children[move]
		else:
			return None

class MoveTree:
	def __init__(self):
		self.board = chess.Board()
		self.root = MoveNode(None, None, self.board.fen())
		self.root.color = chess.WHITE
		self.root.createChildren()
		self.root.moveUCI = "ROOT"
		self.root.score = 0
		self.turnColor = chess.WHITE
		self.zorbistHashedNodes = dict()
		self.MAX_SEARCH_DEPTH = 3

	def expandTree(self):
		totalTime = time.perf_counter()
		i = 0
		path = [self.root]
		while path:
			'''
			i = 1
			if(i % 10000 == 0):
				print('Calcualtions: ' + str(int(i)))
			'''
			currNode = path.pop()
			if not currNode.children and currNode.depth - self.root.depth <= self.MAX_SEARCH_DEPTH:
				currNode.createChildren()

			if currNode.depth - self.root.depth <= self.MAX_SEARCH_DEPTH:
				nodesToDelete = []
				for move in currNode.children:
					currChildNode = currNode.getChild(move)
					#zorbHash = chess.polyglot.zobrist_hash(currChildNode.BitBoard)
					zorbHash = 1

					if zorbHash in self.zorbistHashedNodes and self.zorbistHashedNodes[zorbHash] != currChildNode:
						nodesToDelete.append(move)
					else:
						path.append(currNode.children[move])
						#self.zorbistHashedNodes[zorbHash] = currChildNode
				for move in nodesToDelete:
					currNode.deleteChild(move)
			#if currNode.parent:
			#	currNode.parent.propagateScoreUp(currNode.score, currNode.moveUCI, currNode)
		print(time.perf_counter() - totalTime)

	def minMaxSearch(self):
		nodes = [self.root]
		while nodes:
			currNode = nodes.pop()
			if not currNode.children:
				currNode.minMaxPropagation(currNode.score, currNode.moveUCI, currNode)
			else:
				for move in currNode.children:
					nodes.append(currNode.children[move])



	def makeMove(self, move):
		self.turnColor = not self.turnColor
		chessMove = chess.Move.from_uci(move)
		self.board.push(chessMove)
		currentTurnColor = self.root.color
		if move in self.root.children:
			self.root = self.root.children[move]
			if not self.root.children:
				pdb.set_trace()
				self.root.createChildren()
		else:
			self.root = MoveNode(move, self.root, self.board.fen())
			self.root.createChildren()
		

	def engineMove(self):
		self.expandTree()
		self.minMaxSearch()
		self.makeMove(self.root.optimalMove)

	def play(self):
		self.expandTree()
		while True:
			self.printTree()
			print(self.board)
			if self.turnColor == chess.WHITE:
				userTurnText = input("Enter turn: ")
				try:
					userTurn = chess.Move.from_uci(userTurnText)
				except ValueError:
					print("Move not valid.")
					continue
				#pdb.set_trace()
				self.makeMove(userTurnText)
			else:
				print("Engine Moving...")
				self.engineMove()



	def printTree(self):
		print_tree(self.root, "debugChildrenList")

ai = MoveTree()
#ai.play()

ai.expandTree()
#ai.printTree()


		