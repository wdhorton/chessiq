import pytest
from unittest.mock import mock_open, MagicMock, patch, Mock
from io import StringIO
import hashlib
import pickle
import chess.pgn
from tempfile import TemporaryDirectory
from pathlib import Path
import chessiq.opening_analyzer.analyze
from chessiq.opening_analyzer.analyze import get_fen_collector, analyze, CACHE_DIR

# Mock classes or methods needed for the tests
class MockFenCollector(chess.pgn.BaseVisitor):
    def __init__(self, *args, **kwargs):
        pass

    def accept(self, game):
        pass

    result = Mock()


@pytest.fixture
def mock_repertoire_pgn():
    pgn_data = '[Event "Mock Event"]\n1. e4 e5\n'
    return StringIO(pgn_data)

@pytest.fixture
def mock_game():
    return chess.pgn.Game()


@pytest.fixture
def mock_empty_pgn():
    return StringIO("")


@pytest.fixture
def mock_multiple_games_pgn():
    pgn_data = '[Event "Game 1"]\n1. e4 e5\n\n[Event "Game 2"]\n1. d4 d5\n'
    return StringIO(pgn_data)


@pytest.fixture
def mock_collector():
    with patch("chessiq.opening_analyzer.analyze.FenCollector", autospec = True) as mock:
        yield mock



@pytest.fixture
def mock_cache():
    # Mock the CACHE_DIR 
    with patch('chessiq.opening_analyzer.analyze.CACHE_DIR') as mock:
        yield mock



@pytest.fixture
def mock_pickle():
    with patch('chessiq.opening_analyzer.analyze.pickle') as mock:
        yield mock


# Test function for PGN with multiple games
def test_get_fen_collector_with_multiple_games(mock_collector, mock_cache, mock_pickle, mock_multiple_games_pgn):
    mock_cache.__truediv__.return_value.exists.return_value = False

    fen_collector = get_fen_collector(mock_multiple_games_pgn)

    # You might want to check how many times accept was called, which indicates how many games were parsed.
    # Here, accept would be called twice because there should be two games in mock_multiple_games_pgn
    assert fen_collector.result.call_count == 2


def test_get_fen_collector_uses_cache(mock_repertoire_pgn, mock_collector, mock_pickle, mock_cache):
    get_fen_collector(mock_repertoire_pgn)
    
    assert mock_pickle.load.called_once()

    # assert that FenCollector was not instantiated again (since we're using the cache)
    mock_collector.assert_not_called()


@pytest.mark.parametrize("pgn_str, expected_cache_filename", [
    ('[Event "Mock Event"]\n1. e4 e5\n', hashlib.sha1('[Event "Mock Event"]\n1. e4 e5\n'.encode('utf-8')).hexdigest() + ".pkl"),
])
def test_get_fen_collector_creates_cache_file(mock_repertoire_pgn, pgn_str, expected_cache_filename, mock_cache, mock_pickle):
    # Run function
    fen_collector = get_fen_collector(mock_repertoire_pgn)
    
    # Assert cache file creation
    cache_file = mock_cache /expected_cache_filename
    assert mock_pickle.dump.called_once_with(cache_file)

# Add more tests for edge cases and other scenarios, such as:
# - The repertoire PGN returns an empty string
# - The repertoire PGN has multiple games
# - The cache file already exists

# Define tests for the 'analyze' function
def test_analyze_accepts_game_and_returns_comparison(mock_repertoire_pgn, mocker):
    # Mock the FenCollector and FenComparison to isolate tests
    mocked_fen_collector = mocker.patch("chessiq.opening_analyzer.analyze.get_fen_collector", return_value=MockFenCollector())
    mocked_fen_comparison = MagicMock()

    mocker.patch('chessiq.opening_analyzer.analyze.FenComparison', return_value=mocked_fen_comparison)

    # Mock games PGN
    games_pgn = StringIO('[Event "Another Mock Event"]\n1. d4 d5\n')

    # Run function
    comparison_result = analyze([mock_repertoire_pgn], games_pgn)

    # Assert that accept was called on FenComparison
    # and that the result object is returned
    mocked_fen_comparison.result.assert_called()
    assert comparison_result == mocked_fen_comparison

# ... More tests should follow for different scenarios and edge cases within the analyze function
