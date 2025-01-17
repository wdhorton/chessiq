from functools import cache
import chess
import chess.pgn
from collections import defaultdict
import hashlib
from pathlib import Path
import pickle
from io import StringIO


CACHE_DIR = Path("~/.chessiq/repertoires/").expanduser()
CACHE_DIR.mkdir(exist_ok=True, parents=True)


class FenCollector(chess.pgn.BaseVisitor):
    """
    Visits all moves in a PGN, collecting a set of 
    moves made at a given FEN, as well as the set of
    variations that can lead to a given FEN.
    """
    def __init__(self):
        self.name = ""
        self.fens = defaultdict(set)
        self.variations = defaultdict(set)
        self.pgn_str = ""
    
    def visit_move(self, board, move):
        fen = board.fen().split('-')[0] # we don't care about the move number
        move_san = board.san(move)        
        self.fens[fen].add(move_san)
        self.variations[fen].add(chess.Board().variation_san(board.move_stack))

        board.push(move)
        self.variations[board.fen().split('-')[0]].add(chess.Board().variation_san(board.move_stack))
        board.pop()

    def visit_header(self, tagname, tagvalue):
        if tagname == "Event":
            self.name = tagvalue.split(":")[0]

    def result(self):
        return self

    def to_set(self):
        all_moves = set()

        for fen, move_set in self.fens.items():
            for move in move_set:
                all_moves.add((fen, move))

        return all_moves

    def create_variations(self):
        # TODO: start at starting position, use fens and moves to trace all the variations
        pass

    @classmethod
    def from_set(cls, moves_set):
        instance = cls()
        for fen, move in moves_set:
            instance.fens[fen].add(move)

        instance.create_variations()

        return instance

    @classmethod
    def from_pgn(cls, pgn):
        pgn_str = pgn.read()
        pgn_hash = hashlib.sha1(pgn_str.encode('utf-8')).hexdigest()
        cache_file = CACHE_DIR/f"{pgn_hash}.pkl"
        if cache_file.exists():
            print("loading from cache")
            with cache_file.open("rb") as f:
                return pickle.load(f)
        
        pgn_f = StringIO(pgn_str)
        instance = cls()
        game = chess.pgn.read_game(pgn_f)
        while game:
            game.accept(instance)
            game = chess.pgn.read_game(pgn_f)
        instance.pgn_str = pgn_str

        with cache_file.open("wb") as f:
            pickle.dump(instance, f)

        return instance
    
    @classmethod
    def from_pgns(cls, pgns):
        # TODO: combine PGNs
        pgn_str = pgns[0].read()
        pgn_hash = hashlib.sha1(pgn_str.encode('utf-8')).hexdigest()
        cache_file = CACHE_DIR/f"{pgn_hash}.pkl"
        if cache_file.exists():
            print("loading from cache")
            with cache_file.open("rb") as f:
                return pickle.load(f)
        
        pgn_f = StringIO(pgn_str)
        instance = cls()
        game = chess.pgn.read_game(pgn_f)
        while game:
            game.accept(instance)
            game = chess.pgn.read_game(pgn_f)
        instance.pgn_str = pgn_str

        with cache_file.open("wb") as f:
            pickle.dump(instance, f)

        return instance

    def __hash__(self):
        return hash(self.pgn_str)
