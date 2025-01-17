from collections import defaultdict
import sys
import chess.pgn
from chess.polyglot import zobrist_hash


class MoveRecorder(chess.pgn.BaseVisitor):
    def __init__(self):
        self.game_id = -1
        self.game_metadata = defaultdict(dict)
        
    def begin_game(self):
        self.game_id += 1
        
    def visit_header(self, tagname, tagvalue):
        self.game_metadata[self.game_id][tagname] = tagvalue

    def visit_move(self, board, move):
        dct = {
            "position": zobrist_hash(board),
            "from_square": move.from_square,
            "to_square": move.to_square,
            "promotion": move.promotion,
            "ply": board.ply(),
            "game_id": self.game_id
        }

    def result(self):
        pass


pgn_file = sys.stdin

game = chess.pgn.read_game(pgn_file)

visitor = MoveRecorder()

try:

    while game:
        game.accept(visitor)
        game = chess.pgn.read_game(pgn_file)

except KeyboardInterrupt:
    print()
    print(visitor.game_id)