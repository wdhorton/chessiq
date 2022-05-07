import chess
import chess.pgn
from collections import defaultdict


class FenComparison(chess.pgn.BaseVisitor):
    """
    Compares the positions collected by a FenCollector with another
    PGN, and returns useful metadata on divergences.
    """
    def __init__(self, fen_collector):
        self.fen_collector = fen_collector
        self.divergences = defaultdict(list)
        self.game_id = -1
        self.game_metadata = defaultdict(dict)
        
    def begin_game(self):
        self.game_id += 1
        
    def visit_header(self, tagname, tagvalue):
        self.game_metadata[self.game_id][tagname] = tagvalue
    
    def visit_move(self, board, move):
        fen = board.fen().split('-')[0]
        move_str = board.san(move)
        
        board.push(move)
        new_fen = board.fen().split('-')[0]
        board.pop()

        moves_at_fen = self.fen_collector.fens.get(fen)
        
        if moves_at_fen and move_str not in moves_at_fen:
            self.divergences[self.game_id].append(
                {
                    "position": fen,
                    "move_number": board.fullmove_number, 
                    "player": 'white' if board.turn == chess.WHITE else 'black', 
                    "move": move_str, 
                    "book_moves": moves_at_fen,
                    "variations": self.fen_collector.variations[fen],
                    "url": self.game_metadata[self.game_id].get('Link') or self.game_metadata[self.game_id].get('Site'), 
                    "new_position": new_fen,
                }
            )

    def result(self):
        return self.divergences