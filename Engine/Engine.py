import sys
sys.path.insert(0, '../chess')

import chess
import numpy as np
from pptree import *
import chess.polyglot
import pdb
import time
import OpeningBookCreator
import random
import typing

#Using Piece values and square values from Sunfish Engine
PIECE_VALUES = {
    0: 0,
    chess.PAWN: 100,
    chess.KNIGHT: 280,
    chess.BISHOP: 320,
    chess.ROOK: 479,
    chess.QUEEN: 929,
    chess.KING: 60000
}

SQUARE_VALUES = {
    '0': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    chess.PAWN: (0, 0, 0, 0, 0, 0, 0, 0, 78, 83, 86, 73, 102, 82, 85, 90, 7,
                 29, 21, 44, 40, 31, 44, 7, -17, 16, -2, 15, 14, 0, 15, -13,
                 -26, 3, 10, 9, 6, 1, 0, -23, -22, 9, 5, -11, -10, -2, 3, -19,
                 -31, 8, -7, -37, -36, -14, 3, -31, 0, 0, 0, 0, 0, 0, 0, 0),
    chess.KNIGHT:
    (-66, -53, -75, -75, -10, -55, -58, -70, -3, -6, 100, -36, 4, 62, -4, -14,
     10, 67, 1, 74, 73, 27, 62, -2, 24, 24, 45, 37, 33, 41, 25, 17, -1, 5, 31,
     21, 22, 35, 2, 0, -18, 10, 13, 22, 18, 15, 11, -14, -23, -15, 2, 0, 2, 0,
     -23, -20, -74, -23, -26, -24, -19, -35, -22, -69),
    chess.BISHOP:
    (-59, -78, -82, -76, -23, -107, -37, -50, -11, 20, 35, -42, -39, 31, 2,
     -22, -9, 39, -32, 41, 52, -10, 28, -14, 25, 17, 20, 34, 26, 25, 15, 10,
     13, 10, 17, 23, 17, 16, 0, 7, 14, 25, 24, 15, 8, 25, 20, 15, 19, 20, 11,
     6, 7, 6, 20, 16, -7, 2, -15, -12, -14, -15, -10, -10),
    chess.ROOK:
    (35, 29, 33, 4, 37, 33, 56, 50, 55, 29, 56, 67, 55, 62, 34, 60, 19, 35, 28,
     33, 45, 27, 25, 15, 0, 5, 16, 13, 18, -4, -9, -6, -28, -35, -16, -21, -13,
     -29, -46, -30, -42, -28, -42, -25, -25, -35, -26, -46, -53, -38, -31, -26,
     -29, -43, -44, -53, -30, -24, -18, 5, -2, -18, -31, -32),
    chess.QUEEN:
    (6, 1, -8, -104, 69, 24, 88, 26, 14, 32, 60, -10, 20, 76, 57, 24, -2, 43,
     32, 60, 72, 63, 43, 2, 1, -16, 22, 17, 25, 20, -13, -6, -14, -15, -2, -5,
     -1, -10, -20, -22, -30, -6, -13, -11, -16, -11, -16, -27, -36, -18, 0,
     -19, -15, -15, -21, -38, -39, -30, -31, -13, -31, -36, -34, -42),
    chess.KING:
    (4, 54, 47, -99, -99, 60, 83, -62, -32, 10, 55, 56, 56, 55, 10, 3, -62, 12,
     -57, 44, -67, 28, 37, -31, -55, 50, 11, -4, -19, 13, 0, -49, -55, -43,
     -52, -28, -51, -47, -8, -50, -47, -42, -43, -79, -64, -32, -29, -32, -4,
     3, -14, -50, -57, -18, 13, 4, 17, 30, -3, -14, 6, -1, 40, 18),
}

SQUARES = np.array([
    chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1,
    chess.H1, chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2,
    chess.G2, chess.H2, chess.A3, chess.B3, chess.C3, chess.D3, chess.E3,
    chess.F3, chess.G3, chess.H3, chess.A4, chess.B4, chess.C4, chess.D4,
    chess.E4, chess.F4, chess.G4, chess.H4, chess.A5, chess.B5, chess.C5,
    chess.D5, chess.E5, chess.F5, chess.G5, chess.H5, chess.A6, chess.B6,
    chess.C6, chess.D6, chess.E6, chess.F6, chess.G6, chess.H6, chess.A7,
    chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7,
    chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8,
    chess.H8
])


class TTEntry:
    EXACT = 0
    ALPHA = 1
    BETA = 2

    def __init__(self, hashVal, move, depth, value, flag):
        self.hash = hashVal
        self.move = move
        self.depth = depth
        self.value = value
        self.ancient = True
        self.flag = flag


class TranspositionTable:
    def __init__(self):
        self.SIZE = 10**6
        self.table = np.empty(self.SIZE, dtype=np.dtype(TTEntry))
        #TableStats
        self.entries = 0
        self.lookupMatches = 0
        self.lookupMisses = 0
        self.totalLookups = 0
        self.collisions = 0
        self.totalTableTime = 0

    def getTableStatString(self):
        return "Total Entries: {} \nTotal Lookups: {} \nLookup Matches: {} \nLookup Misses: {}\nCollisions: {} \nTotal Time Spent in Table: {} \n".format(
            self.entries, self.totalLookups, self.lookupMatches,
            self.lookupMisses, self.collisions, self.totalTableTime)

    def resetTableStates(self):
        self.entries = 0
        self.lookupMatches = 0
        self.totalLookups = 0
        self.collisions = 0
        self.totalTableTime = 0

    def getEntry(self, hashVal):
        startTime = time.perf_counter()
        self.totalLookups += 1
        hashMod = hashVal % self.SIZE
        if self.table[hashMod]:
            entry = self.table[hashMod]
            entry.ancient = False
            self.lookupMatches += 1
            self.totalTableTime += time.perf_counter() - startTime
            return entry
        else:
            self.lookupMisses += 1
            self.totalTableTime += time.perf_counter() - startTime
            return None

    def addEntry(self, hashVal, entry):
        startTime = time.perf_counter()
        hashMod = hashVal % self.SIZE
        if self.table[hashMod]:
            if self.table[hashMod].hash != hashVal:
                self.collisions += 1
        else:
            self.entries += 1
        self.table[hashMod] = entry
        self.totalTableTime += time.perf_counter() - startTime

    def isEntry(self, hashVal):
        self.totalLookups += 1
        startTime = time.perf_counter()
        hashMod = hashVal % self.SIZE
        entry = self.table[hashMod]
        if entry and entry.hash == hashVal:
            self.lookupMatches += 1
            self.totalTableTime += time.perf_counter() - startTime
            return True
        else:
            self.lookupMisses += 1
            self.totalTableTime += time.perf_counter() - startTime
            return False


class MoveTree:
    def __init__(self):
        self.board = chess.Board()
        self.MAX_SEARCH_DEPTH = 1000
        self.engineColor = chess.BLACK
        self.table = TranspositionTable()
        self.OpeningBookCreator = OpeningBookCreator.OpeningBookCreator(
            "../env/Lib/site-packages/chess/data/polyglot/SmileyInitOpen.bin")
        self.OpeningBook = chess.polyglot.open_reader(
            "../env/Lib/site-packages/chess/data/polyglot/performance.bin")
        self.Killers = []
        self.Countermoves = np.zeros((64, 64), dtype=np.dtype(chess.Move))
        self.RANDOM_HASH_ARRAY = chess.polyglot.POLYGLOT_RANDOM_ARRAY
        self.zorbistHasherObj = chess.polyglot.ZobristHasher(
            self.RANDOM_HASH_ARRAY)
        #For debugging perposes
        self.tableALPHA = 0
        self.tableBETA = 0
        self.tableEXACT = 0
        self.movesReordered = 0
        self.searchStart = None
        self.totalNodesSearched = 0
        self.transitionTablePruning = 0
        self.totalNodesPruned = 0
        self.averageDepthPruned = 0
        self.averageTransitionTablePrune = 0
        self.openingBookHits = 0
        self.killersFound = 0
        self.timeForLibrary = 0

    def setSearchStats(self):
        self.timeForLibrary = 0
        self.openingBookHits = 0
        self.tableEXACT = 0
        self.tableALPHA = 0
        self.tableBETA = 0
        self.movesReordered = 0
        self.totalNodesSearched = 0
        self.transitionTablePruning = 0
        self.totalNodesPruned = 0
        self.averageDepthPruned = 0
        self.averageTransitionTablePrune = 0
        self.searchStart = time.perf_counter()

    def printSearchStats(self):
        totalTime = time.perf_counter() - self.searchStart
        treeStatString = "Total Nodes Searched: {}\nTable Nodes Pruned: {}\nAverage Table Pruned Node Depth: {}\nEXACT: {}\nALPHA: {}\nBETA: {}\nMoves Reodered: {}\nTotal Search Nodes Pruned: {}\nAverage Search Node Pruned Depth: {}\nOpening Book Hits: {}\nKillers Found: {}\nTotal Time For Searches: {} \nLibrary Time: {}\n".format(
            self.totalNodesSearched, self.transitionTablePruning,
            self.averageTransitionTablePrune, self.tableEXACT, self.tableALPHA,
            self.tableBETA, self.movesReordered, self.totalNodesPruned,
            self.averageDepthPruned, self.openingBookHits, self.killersFound,
            totalTime, self.timeForLibrary)
        tableStatString = self.table.getTableStatString()
        print(tableStatString + treeStatString)

    def evaluateBoardScore(self, board):
        if board.result() != "*":
            if (board.result() == "0-1" and self.engineColor
                    == chess.WHITE) or (board.result() == "0-1"
                                        and self.engineColor == chess.BLACK):
                return 10**7
            elif (board.result() == "1-0" and self.engineColor
                  == chess.BLACK) or (board.result() == "1-0"
                                      and self.engineColor == chess.WHITE):
                return -10**7
            elif board.result() == "1/2-1/2":
                return 0
        whiteScore = 0
        blackScore = 0
        for i in range(64):
            piece = self.board.piece_at(SQUARES[i])
            if piece and piece.color == chess.WHITE:
                whiteScore += PIECE_VALUES[piece.piece_type] + SQUARE_VALUES[
                    piece.piece_type][i]
            elif piece:
                blackScore += PIECE_VALUES[piece.piece_type] + SQUARE_VALUES[
                    piece.piece_type][63 - i]
        return (blackScore - whiteScore)

    def findBestMove(self):
        init_moves = self.board.legal_moves
        bestMove = None
        self.Killers = []
        boardHash = chess.polyglot.zobrist_hash(self.board,
                                              _hasher=self.zorbistHasherObj)
        start = time.time()
        for i in range(1, self.MAX_SEARCH_DEPTH + 1):
            alpha = -np.inf
            beta = np.inf
            currVal, currMove = self.alphaBetaPrune(i, alpha, beta, True,
                                                    self.engineColor, 0, boardHash, start)
            if currMove:
                bestMove = currMove
            if time.time() - start > 1:
                print(i)
                print(time.time() - start)
                break
        if not bestMove:
            print("Could not find move")
            return init_moves[0]
        return bestMove

    def takeTurn(self, move):
        if isinstance(move, str):
            chessMove = chess.Move.from_uci(move)
            if chessMove not in self.board.legal_moves:
                raise AssertionError

            self.board.push(chessMove)
            return
        elif isinstance(move, chess.Move):
            self.board.push(move)
            return

    def play(self):
        self.turnColor = chess.WHITE
        while True:
            print(self.board)
            if self.turnColor == chess.WHITE:
                usrMove = input("Type Move: ")
                if (usrMove == "back"):
                    continue
                try:
                    self.takeTurn(usrMove)
                except ValueError:
                    print("Error wrong format.")
                    continue
                except AssertionError:
                    print("Invalid Move.")
                    continue
                self.turnColor = not self.turnColor
            else:
                self.searchStart = time.perf_counter()
                engineMove = self.findBestMove()
                self.printSearchStats()
                self.takeTurn(engineMove)
                self.turnColor = not self.turnColor
            print("\n\n")

    def tableLookup(self, hashVal):
        '''
        hashVal = chess.polyglot.zobrist_hash(self.board,
                                              _hasher=self.zorbistHasherObj)
        '''
        if self.table.isEntry(hashVal):
            return self.table.getEntry(hashVal)
        else:
            return None

    def addCurrentStateToTable(self, move, depth, value, flag, hashVal):
        '''
        hashVal = chess.polyglot.zobrist_hash(self.board,
                                              _hasher=self.zorbistHasherObj)
        '''
        entry = TTEntry(hashVal, move, depth, value, flag)
        self.table.addEntry(hashVal, entry)
        return

    def putMoveAtFront(self, moveSet, move):
        temp = moveSet[0]
        moveIndex = None
        for i in range(len(moveSet)):
            if moveSet[i] == move:
                moveIndex = i
                break
        if moveIndex:
            moveSet[moveIndex] = temp
            moveSet[0] = move
        return moveSet

    def isMoveCapture(self, move):
        moveFrom = move.from_square
        moveTo = move.to_square
        if self.board.piece_at(
                moveTo) and 1 <= self.board.piece_at(moveTo).piece_type <= 6:
            return True
        else:
            return False

    def addToKillers(self, move, distance):
        while len(self.Killers) <= distance:
            self.Killers.append(set())
        if move not in self.Killers[distance]:
            self.Killers[distance].add(move)
        if self.isMoveCapture(move):
            self.Countermoves[move.from_square][move.to_square] = move

    def sortMoves(self, moveSet, depth, distance, optimalMove):
        moveArray = []
        ordering = []
        for move in moveSet:
            moveArray.append(move)
            ordering.append(0)
            if move == optimalMove:
                ordering[-1] += 10000
                continue
            if distance < len(self.Killers):
                if move in self.Killers[distance]:
                    ordering[-1] += 1
                    self.killersFound += 1
                if distance >= 1 and move in self.Killers[distance - 1]:
                    ordering[-1] += 1
                    self.killersFound += 1
                if distance + 1 < len(
                        self.Killers) and move in self.Killers[distance + 1]:
                    ordering[-1] += 1
                    self.killersFound += 1
            if self.isMoveCapture(move):
                ordering[-1] += PIECE_VALUES[self.board.piece_at(
                    move.to_square).piece_type] / 100
            if self.Countermoves[move.from_square][move.to_square] == move:
                ordering[-1] += 1
        return [
            x for _, x in sorted(
                zip(ordering, moveArray), key=lambda x: x[0], reverse=True)
        ]

    def calculateNewZorbistHash(self, oldHash, move):
        #First check metadata for current castling rights and current en_passant
        currentCastlingRights = self.zorbistHasherObj.hash_castling(self.board) 
        currentEnPassantRights = self.zorbistHasherObj.hash_ep_square(self.board)
        #Four values to be determined
            #Original source hash
            #Original destination hash
            #Updated destination hash
        sourceHash = 0
        destinationHash = 0
        updatedDestinationHash = 0
        #Move has source location and destination location
        source = move.from_square
        destination = move.to_square
        sourcePiece = self.board.piece_at(source)
        destinationPiece = self.board.piece_at(destination)
        if sourcePiece:
            sourcePieceIndex = (sourcePiece.piece_type - 1) * 2
            sourcePieceIndex += 1 if sourcePiece.color else 0
            sourceHash = self.RANDOM_HASH_ARRAY[64*sourcePieceIndex + source]
            if move.promotion:
                promotedPieceType = move.promotion
                promotionIndex = (promotedPieceType-1)*2
                promotionIndex += 1 if sourcePiece.color else 0
                updatedDestinationHash = self.RANDOM_HASH_ARRAY[64*promotionIndex + destination]
            else:
                updatedDestinationHash = self.RANDOM_HASH_ARRAY[64*sourcePieceIndex + destination]
        #Must check if move is castling
        if self.board.is_castling(move):
            rookIndex = 7 if sourcePiece.color else 6
            if self.board.is_kingside_castling(move):
                if sourcePiece.color:
                    destinationHash ^= (self.RANDOM_HASH_ARRAY[64*rookIndex + chess.H1]
                                        ^ self.RANDOM_HASH_ARRAY[64*rookIndex + chess.F1])
                else:
                    destinationHash ^= (self.RANDOM_HASH_ARRAY[64*rookIndex + chess.H8]
                                        ^ self.RANDOM_HASH_ARRAY[64*rookIndex + chess.F8])
            elif self.board.is_queenside_castling(move):
                if sourcePiece.color:
                    destinationHash ^= (self.RANDOM_HASH_ARRAY[64*rookIndex + chess.A1]
                                        ^ self.RANDOM_HASH_ARRAY[64*rookIndex + chess.D1])
                else:
                    destinationHash ^=  (self.RANDOM_HASH_ARRAY[64*rookIndex + chess.A8]
                                        ^ self.RANDOM_HASH_ARRAY[64*rookIndex + chess.D8])
        else:    
            #If not castling simply use this to remove the piece bit string from hash
            if destinationPiece:
                destinationPieceIndex = (destinationPiece.piece_type - 1)*2
                destinationPieceIndex += 1 if destinationPiece.color else 0
                destinationHash = self.RANDOM_HASH_ARRAY[64*destinationPieceIndex + destination]
        aug = sourceHash ^ updatedDestinationHash ^ destinationHash ^  self.zorbistHasherObj.hash_turn(self.board)
        self.board.push(move)
        if currentCastlingRights != self.zorbistHasherObj.hash_castling(self.board) and currentEnPassantRights != self.zorbistHasherObj.hash_ep_square(self.board):
            hashWithoutOtherData = (  oldHash 
                                    ^ aug 
                                    ^ self.zorbistHasherObj.hash_turn(self.board) 
                                    ^ currentCastlingRights 
                                    ^ self.zorbistHasherObj.hash_castling(self.board)
                                    ^ currentEnPassantRights
                                    ^ self.zorbistHasherObj.hash_ep_square(self.board))
        elif currentCastlingRights != self.zorbistHasherObj.hash_castling(self.board):
            hashWithoutOtherData = (  oldHash 
                                    ^ aug 
                                    ^ self.zorbistHasherObj.hash_turn(self.board) 
                                    ^ currentCastlingRights 
                                    ^ self.zorbistHasherObj.hash_castling(self.board))
        elif currentEnPassantRights != self.zorbistHasherObj.hash_ep_square(self.board):
            hashWithoutOtherData = (  oldHash 
                                    ^ aug 
                                    ^ self.zorbistHasherObj.hash_turn(self.board) 
                                    ^ currentEnPassantRights
                                    ^ self.zorbistHasherObj.hash_ep_square(self.board))
        else:
            hashWithoutOtherData = oldHash ^ aug ^ self.zorbistHasherObj.hash_turn(self.board)
        self.board.pop()
        return hashWithoutOtherData


    def alphaBetaPrune(self, depth, alpha, beta, isEngineMove, engineIsWhite,
                       distance, oldHash, searchStartTime):
        self.totalNodesSearched += 1
        tableEntry = self.tableLookup(oldHash)
        if tableEntry and tableEntry.move:
            potentialMoves = self.sortMoves(self.board.legal_moves, depth,
                                            distance, tableEntry.move)
        else:
            potentialMoves = self.sortMoves(self.board.legal_moves, depth,
                                            distance, None)

        if not potentialMoves or depth == 0:
            boardScore = self.evaluateBoardScore(self.board)
            self.addCurrentStateToTable(None, depth, boardScore, TTEntry.EXACT, oldHash)
            return (boardScore, None)

        if isEngineMove:
            bestValue = None
            bestMove = None
            if tableEntry and tableEntry.depth >= depth:
                if tableEntry.flag == TTEntry.EXACT:
                    self.tableEXACT += 1
                    return (tableEntry.value, tableEntry.move)
                elif tableEntry.flag == TTEntry.ALPHA and alpha < tableEntry.value:
                    self.tableALPHA += 1
                    alpha = tableEntry.value
                elif tableEntry.flag == TTEntry.BETA and beta > tableEntry.value:
                    beta = tableEntry.value
                if beta <= alpha:
                    self.transitionTablePruning += 1
                    self.averageTransitionTablePrune = (
                        ((self.transitionTablePruning - 1) *
                         self.averageTransitionTablePrune) +
                        depth) / self.transitionTablePruning
                    if tableEntry.move:
                        self.addToKillers(tableEntry.move, distance)
                    return (alpha, tableEntry.move)

            for move in potentialMoves:
                #Stop search if to much time passed
                if time.time() - searchStartTime > 2:
                    return (None, None)
                newHash = self.calculateNewZorbistHash(oldHash, move)
                self.board.push(move)
                '''
                actualStateHash = chess.polyglot.zobrist_hash(self.board,
                                              _hasher=self.zorbistHasherObj)
                if newHash == actualStateHash:
                    #print("Black")
                    #print("Yes")
                    dummy = 0
                else:
                    print("Black")
                    print(self.board)
                    print("Calculated Hash: " + str(bin(newHash)) + "\n" + 
                         "Actual Hash:      " + str(bin(actualStateHash)) + "\n" + 
                         "Old Hash:         " + str(bin(oldHash))) 
                '''               
                currBoardValue = self.alphaBetaPrune(depth - 1, alpha, beta,
                                                     not isEngineMove,
                                                     engineIsWhite,
                                                     distance + 1, newHash, searchStartTime)[0]
                self.board.pop()
                if move.uci() == "h8g8" or move.uci() == "a8b8":
                    print("----")
                    print("White") if self.board.turn else print("Black")
                    print("Alpha: "+ str(alpha))
                    print("Beta: "+str(beta))
                    print("Value: "+str(currBoardValue))
                    print("Best Value: " + str(bestValue))
                    print("Depth: "+str(depth))
                    if bestValue and currBoardValue and  currBoardValue > bestValue:
                        print(self.board)
                    print("----")
                if not currBoardValue:
                    continue
                if currBoardValue > alpha:
                    alpha = currBoardValue
                    bestValue = currBoardValue
                    bestMove = move
                '''    
                if not bestValue or currBoardValue > bestValue:
                    bestValue = currBoardValue
                    bestMove = move
                if bestValue > alpha:
                    alpha = bestValue
                '''
                if beta <= alpha:
                    self.addCurrentStateToTable(bestMove, depth, bestValue,
                                                TTEntry.ALPHA, newHash)
                    self.totalNodesPruned += 1
                    self.averageDepthPruned = ((self.averageDepthPruned *
                                                (self.totalNodesPruned - 1)) +
                                               depth) / self.totalNodesPruned
                    self.addToKillers(move, distance + 1)
                    return (bestValue, bestMove)
            self.addCurrentStateToTable(bestMove, depth, bestValue,
                                        TTEntry.EXACT, oldHash)
            return (bestValue, bestMove)

        else:
            bestValue = None
            bestMove = None
            if tableEntry and tableEntry.depth >= depth:
                if tableEntry.flag == TTEntry.EXACT:
                    self.tableEXACT += 1
                    return (tableEntry.value, tableEntry.move)
                elif tableEntry.flag == TTEntry.ALPHA and alpha < tableEntry.value:
                    alpha = tableEntry.value
                elif tableEntry.flag == TTEntry.BETA and beta > tableEntry.value:
                    self.tableBETA += 1
                    beta = tableEntry.value

                if beta <= alpha:
                    self.transitionTablePruning += 1
                    self.averageTransitionTablePrune = (
                        ((self.transitionTablePruning - 1) *
                         self.averageTransitionTablePrune) +
                        depth) / self.transitionTablePruning
                    if tableEntry.move:
                        self.addToKillers(tableEntry.move, distance)
                    return (beta, tableEntry.move)

            for move in potentialMoves:
                if time.time() - searchStartTime > 2:
                    return (None, None)
                newHash = self.calculateNewZorbistHash(oldHash, move)
                self.board.push(move)
                '''
                actualStateHash = chess.polyglot.zobrist_hash(self.board,
                                              _hasher=self.zorbistHasherObj)
                if newHash == actualStateHash:
                    dummy = 0
                else:
                    print("White")
                    print(self.board)
                    print("Calculated Hash: " + str(bin(newHash)) + "\n" + 
                          "Actual Hash:     " + str(bin(actualStateHash)) + "\n" + 
                          "Old Hash:        " + str(bin(oldHash)))
                '''
                currBoardValue = self.alphaBetaPrune(depth - 1, alpha, beta,
                                                     not isEngineMove,
                                                     engineIsWhite,
                                                     distance + 1, newHash, searchStartTime)[0]
                self.board.pop()
                if not currBoardValue:
                    continue
                if beta > currBoardValue:
                    beta = currBoardValue
                    bestMove = move
                    bestValue = currBoardValue
                '''
                if not bestValue or currBoardValue < bestValue:
                    bestValue = currBoardValue
                    bestMove = move
                if bestValue < beta:
                    beta = bestValue
                '''
                if beta <= alpha:
                    self.addCurrentStateToTable(bestMove, depth, bestValue,
                                                TTEntry.BETA, newHash)
                    self.totalNodesPruned += 1
                    self.averageDepthPruned = ((self.averageDepthPruned *
                                                (self.totalNodesPruned - 1)) +
                                               depth) / self.totalNodesPruned
                    self.addToKillers(move, distance + 1)
                    return (bestValue, bestMove)

            self.addCurrentStateToTable(bestMove, depth, bestValue,
                                        TTEntry.EXACT, oldHash)
            return (bestValue, bestMove)
ai = MoveTree()
ai.play()