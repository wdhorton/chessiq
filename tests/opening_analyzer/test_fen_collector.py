from io import StringIO

import chess.pgn

from chessiq.opening_analyzer.fen_collector import FenCollector

def test_to_set():
    pgn = StringIO("1. e4 e5 2. Nf3 Nc6")

    game = chess.pgn.read_game(pgn)

    fen_collector = FenCollector()

    game.accept(fen_collector)

    actual = fen_collector.to_set()

    expected = {
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq ", "e4"),
        ("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq ", "e5"),
        ("rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq ", "Nf3"),
        ("rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq ", "Nc6"),
    }

    assert actual == expected


def test_from_set():
    test_set = {
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq ", "e4"),
        ("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq ", "e5"),
        ("rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq ", "Nf3"),
        ("rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq ", "Nc6"),
    }

    fen_collector = FenCollector.from_set(test_set)

    expected = {
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq ": {"e4"},
        "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq ":  {"e5"},
        "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq ": {"Nf3"},
        "rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq ": {"Nc6"},
    }

    assert fen_collector.fens == expected


def test_hash_same():
    fen_collector1 = FenCollector.from_pgn(StringIO("1. e4 e5 2. Nf3 Nc6"))
    fen_collector2 = FenCollector.from_pgn(StringIO("1. e4 e5 2. Nf3 Nc6"))

    assert hash(fen_collector1) == hash(fen_collector2)


def test_hash_different():
    fen_collector1 = FenCollector.from_pgn(StringIO("1. e4 e5 2. Nf3 Nc6"))
    fen_collector2 = FenCollector.from_pgn(StringIO("1. e4 e5 2. Nf3 Nf6"))

    assert hash(fen_collector1) != hash(fen_collector2)