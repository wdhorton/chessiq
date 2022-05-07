import chess.pgn

from .fen_collector import FenCollector
from .fen_comparison import FenComparison


def analyze(repertoire_pgn, games_pgn):
    fen_collector = FenCollector()

    game = chess.pgn.read_game(repertoire_pgn)
    while game:
        game.accept(fen_collector)
        game = chess.pgn.read_game(repertoire_pgn)

    fen_comparison = FenComparison(fen_collector)

    game = chess.pgn.read_game(games_pgn)
    while game:
        game.accept(fen_comparison)
        game = chess.pgn.read_game(games_pgn)


    return fen_comparison.divergences