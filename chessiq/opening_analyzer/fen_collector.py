import chess
import chess.pgn
from collections import defaultdict


class FenCollector(chess.pgn.BaseVisitor):
    """
    Visits all moves in a PGN, collecting a set of 
    moves made at a given FEN, as well as the set of
    variations that can lead to a given FEN.
    """
    def __init__(self):
        self.fens = defaultdict(set)
        self.variations = defaultdict(set)
    
    def visit_move(self, board, move):
        fen = board.fen().split('-')[0] # we don't care about the move number
        move = board.san(move)        
        self.fens[fen].add(move)
        self.variations[fen].add(chess.Board().variation_san(board.move_stack))

    def result(self):
        return self