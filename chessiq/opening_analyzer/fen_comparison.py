import chess
import chess.pgn
from collections import defaultdict
from functools import partial

from .engine import analyze_position
from .lichess_api import get_frequency_of_position


class FenComparison(chess.pgn.BaseVisitor):
    """
    Compares the positions collected by FenCollectors with another
    PGN, and returns useful metadata on divergences.
    """
    def __init__(self, fen_collectors, config=None):
        self.fen_collectors = fen_collectors
        self.divergences = defaultdict(list)
        self.game_id = -1
        self.game_metadata = defaultdict(dict)
        self.furthest_move = defaultdict(partial(defaultdict, dict))
        self.config = config
        
    def begin_game(self):
        self.game_id += 1

    def end_game(self):
        repertoire_options = {fen_collector.name for fen_collector in self.fen_collectors}
        repertoire_divergences = {d["repertoire"] for d in self.divergences[self.game_id]}
        repertoires_no_divergence = repertoire_options - repertoire_divergences

        if repertoires_no_divergence:
            self.divergences[self.game_id] = []
            self.furthest_move[self.game_id] = max([self.furthest_move[self.game_id][rep] for rep in repertoires_no_divergence], key=lambda d: int(d["move_number"]))
        else:
            # process divergences, taking only those belonging to the repertoire with the latest (first?) divergence or no divergence
            if self.divergences[self.game_id]:
                repertoire = self.divergences[self.game_id][-1]["repertoire"]
                self.divergences[self.game_id] = [d for d in self.divergences[self.game_id] if d["repertoire"] == repertoire]
                self.furthest_move[self.game_id] = self.furthest_move[self.game_id][repertoire]

    def visit_header(self, tagname, tagvalue):
        self.game_metadata[self.game_id][tagname] = tagvalue
    
    def visit_move(self, board, move):
        fen = board.fen().split('-')[0]
        move_str = board.san(move)
        
        board.push(move)
        new_fen = board.fen().split('-')[0]
        board.pop()

        moves_at_fen_by_collector = [fen_collector.fens.get(fen) for fen_collector in self.fen_collectors]
                
        for moves_at_fen, fen_collector in zip(moves_at_fen_by_collector, self.fen_collectors):
            if moves_at_fen:
                if move_str not in moves_at_fen:
                    board.push(move)
                    new_eval = analyze_position(board)
                    board.pop()

                    best_move_eval = None
                    for possible_move_str in moves_at_fen:
                        board.push(board.parse_san(possible_move_str))
                        move_eval = analyze_position(board)
                        board.pop()
                        if best_move_eval is None or move_eval > best_move_eval:
                            best_move_eval = move_eval

                    eval_diff = (new_eval - move_eval) / 100

                    self.divergences[self.game_id].append(
                        {
                            "type": "divergence",
                            "position": fen,
                            "move_number": board.fullmove_number, 
                            "player": 'white' if board.turn == chess.WHITE else 'black', 
                            "move": move_str, 
                            "book_moves": list(moves_at_fen),
                            "eval_diff": eval_diff,
                            "abs_eval_diff": abs(eval_diff),
                            "db_frequency": get_frequency_of_position(board, self.config["db_start_date"], self.config["db_end_date"], self.config["db_time_controls"], self.config["db_ratings"]),
                            "variations": list(fen_collector.variations[fen]),
                            "result": self.game_metadata[self.game_id].get('Result'),
                            "white_elo": int(self.game_metadata[self.game_id].get('WhiteElo', 0)),
                            "black_elo": int(self.game_metadata[self.game_id].get('BlackElo', 0)),
                            "start_time_utc": self.game_metadata[self.game_id].get('UTCDate', "") + "T" + self.game_metadata[self.game_id].get("UTCTime", ""),
                            "url": self.game_metadata[self.game_id].get('Link'), 
                            "new_position": new_fen,
                            "repertoire": fen_collector.name
                        }
                    )
                else:
                    if self.furthest_move[self.game_id][fen_collector.name].get("ply", -1) < board.ply():
                        self.furthest_move[self.game_id][fen_collector.name] = {
                            "type": "furthest_move",
                            "position": fen,
                            "move_number": board.fullmove_number, 
                            "player": 'white' if board.turn == chess.WHITE else 'black', 
                            "move": move_str, 
                            "variations": list(fen_collector.variations[fen]),
                            "url": self.game_metadata[self.game_id].get('Link'), 
                            "repertoire": fen_collector.name
                        }

    def result(self):
        return self.divergences