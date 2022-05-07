from io import StringIO
from pprint import pprint

import click

from .analyze import analyze
from .lichess_api import get_game, get_study


@click.command()
@click.option("--repertoire_pgn", type=click.File('r'))
@click.option("--games_pgn", type=click.File('r'))
@click.option("--game_id")
@click.option("--study_id")
def analyze_opening(repertoire_pgn, games_pgn, game_id, study_id):
    """
    Run opening analysis.
    """
    if not (games_pgn or game_id):
        raise Exception("Must specify --games_pgn or --game_id")

    if not (repertoire_pgn or study_id):
        raise Exception("Must specify --repertoire_pgn or --study_id")

    if game_id:
        games_pgn = StringIO(get_game(game_id[:8]))

    if study_id:
        repertoire_pgn = StringIO(get_study(study_id))

    divergences = analyze(repertoire_pgn, games_pgn)
    pprint(list(divergences.values()), sort_dicts=False)