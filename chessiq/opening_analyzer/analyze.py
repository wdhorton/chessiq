from pathlib import Path
import pickle
from io import StringIO
import hashlib
import logging

import chess.pgn

from .fen_collector import FenCollector
from .fen_comparison import FenComparison


def analyze(repertoire_pgn, games_pgn, config=None):
    fen_collectors = [FenCollector.from_pgn(pgn) for pgn in repertoire_pgn]

    fen_comparison = FenComparison(fen_collectors, config=config)

    game = chess.pgn.read_game(games_pgn)
    while game:
        game.accept(fen_comparison)
        game = chess.pgn.read_game(games_pgn)

    return fen_comparison