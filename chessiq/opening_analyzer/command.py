import csv
from io import StringIO
import json
import itertools
import sys
from operator import itemgetter
import time

import click
import nltk

from chessiq.config_manager.config import get_config

from .fen_collector import FenCollector
from .analyze import analyze
from . import lichess_api, chess_com_api


@click.group()
def opening():
    pass


@opening.command()
@click.option("--repertoire_pgn", "-r", type=click.File('r'), multiple=True, default=get_config("repertoire_pgn"), help="The path to one or multiple PGN files representing the player's opening repertoire. This option can be specified multiple times if multiple PGNs need to be included. Defaults can be loaded from config.")
@click.option("--games_pgn_file", type=click.File('r'), help="A readable file in PGN format containing the games to be analyzed.")
@click.option("--game_id", help="A specific game ID to analyze. If the ID consists only of digits, it refers to a game from chess.com. Otherwise, it is treated as a Lichess game ID.")
@click.option("--study_id", multiple=True, help="The ID of a study from Lichess to use as a repertoire. This option can be specified multiple times for multiple studies.")
@click.option("--games_pgn_str", help="A string containing game data in PGN format.")
@click.option("--sort_by", help="Defines how the analysis results should be sorted. Can include the sort fields and direction (asc/desc).")
@click.option("--format", default=get_config("format"), help="Output format of the results. Can be 'json' or 'csv'.ß")
@click.option("--db_start_date", default=get_config("db_start_date"), help="The start date for the database games to include in the analysis.")
@click.option("--db_end_date", default=get_config("db_end_date"), help="The end date for the database games to include in the analysis.")
@click.option("--db_time_controls", default=get_config("db_time_controls"), help="A comma-separated string that specifies the time controls of the games to include in the analysis (e.g., blitz,rapid,classical).")
@click.option("--db_ratings", default=get_config("db_ratings"), help="A comma-separated string specifying rating categories for the games to include in the analysis (e.g., 1600,1800,2000,2200,2500).")
@click.option("--username", default=get_config("username"), help="The username of the player for whom the analysis is conducted.")
def analyze_games(repertoire_pgn, games_pgn_file, game_id, study_id, games_pgn_str, sort_by, format, db_start_date, db_end_date, db_time_controls, db_ratings, username):
    """
    Runs opening analysis for the specified chess games.
    """
    if not (games_pgn_file or game_id or games_pgn_str):
        if not username:
            raise Exception("Must specify --games_pgn, --game_id, or --games_pgn_str")
        games_pgn_str = lichess_api.get_latest_game(username)

    if not (repertoire_pgn or study_id):
        raise Exception("Must specify --repertoire_pgn or --study_id")

    if game_id:
        if game_id.isdigit():
            games_pgn = StringIO(chess_com_api.get_game(game_id, username))
        else:
            games_pgn = StringIO(lichess_api.get_game(game_id[:8]))
    elif games_pgn_str:
        games_pgn = StringIO(games_pgn_str)
    else:
        games_pgn = games_pgn_file

    if study_id:
        repertoire_pgn = [StringIO(lichess_api.get_study(sid)) for sid in study_id]

    

    analysis_config = {
        "db_start_date": db_start_date,
        "db_end_date": db_end_date,
        "db_time_controls": db_time_controls, 
        "db_ratings": db_ratings
    }

    fen_comparison = analyze(repertoire_pgn, games_pgn, config=analysis_config)
    result = []
    for divergences, furthest_move in itertools.zip_longest(fen_comparison.divergences.values(), fen_comparison.furthest_move.values()):
        result.extend(divergences)
        result.extend([furthest_move])

    if sort_by:
        phrases = sort_by.split(',')

        for phrase in reversed(phrases):
            if ' ' in phrase:
                sort_key, asc_desc = phrase.strip().split()
            else:
                sort_key = phrase.strip()
                asc_desc = False

            reverse = (asc_desc and asc_desc.strip().lower() == 'desc')
            print(sort_key, reverse)

            result.sort(key=itemgetter(sort_key), reverse=reverse)
    
    if format == 'json':
        print(json.dumps(result, indent=4))
    elif format == 'csv':
        keys = result[0].keys()

        dict_writer = csv.DictWriter(sys.stdout, keys)
        dict_writer.writeheader()
        dict_writer.writerows(result)


@opening.command()
@click.argument("fen")
@click.option("--repertoire_pgn", type=click.File('r'), multiple=True, default=get_config("repertoire_pgn"), help="The path to one or multiple PGN files representing the player's opening repertoire. This option can be specified multiple times if multiple PGNs need to be included. Defaults can be loaded from config.")
@click.option("--study_id", multiple=True, help="The ID of a study from Lichess to use as a repertoire. This option can be specified multiple times for multiple studies.")
def get_moves(fen, repertoire_pgn, study_id):
    """Fetches and prints the moves and variations for a given FEN from a PGN file or a Lichess study."""
    if study_id:
        repertoire_pgn = [StringIO(lichess_api.get_study(sid)) for sid in study_id]

    fen_collector = FenCollector.from_pgn(repertoire_pgn)

    fen = fen.split('-')[0]

    print(fen_collector.fens.get(fen))
    print(fen_collector.variations.get(fen))


def convert_fen_numbers(fen):
    out = []
    for ch in fen:
        if ch.isdigit():
            out.append('-' * int(ch))
        else:
            out.append(ch)
    return ''.join(out).split(' ')[0]


def convert_fen_back(fen):
    out = []
    count = 0
    for ch in fen:
        if ch == '-':
            count += 1
        else:
            if count > 0:
                out.append(str(count))
                count = 0
            out.append(ch)
    
    if count > 0:
        out.append(str(count))
    return ''.join(out).split(' ')[0]


@opening.command()
@click.argument("fen")
@click.option("--repertoire_pgn", type=click.File('r'), multiple=True, default=get_config("repertoire_pgn"), help="The path to one or multiple PGN files representing the player's opening repertoire. This option can be specified multiple times if multiple PGNs need to be included. Defaults can be loaded from config.")
@click.option("--study_id", multiple=True, help="The ID of a study from Lichess to use as a repertoire. This option can be specified multiple times for multiple studies.")
def closest_position(fen, repertoire_pgn, study_id):
    """Finds and prints the closest positions to a given FEN in a player's repertoire or study."""
    if study_id:
        repertoire_pgn = [StringIO(lichess_api.get_study(sid)) for sid in study_id]

    fen_collector = FenCollector.from_pgn(repertoire_pgn)

    fen = convert_fen_numbers(fen.split('-')[0])

    rep_fens = {convert_fen_numbers(fen): fen for fen in fen_collector.fens.keys()}

    print(sorted([(nltk.edit_distance(fen, rep_fen_num), rep_fen) for rep_fen_num, rep_fen in rep_fens.items()])[:5])


@opening.command()
@click.argument("fen")
def reverse_position(fen):
    """Prints the reversed FEN, as if Black were White and vice versa."""
    fen, meta = fen.split(" ", 1)
    rows = fen.split("/")
    new_fen = '/'.join(''.join(c.upper() if c.islower() else c.lower() for c in row) for row in reversed(rows))
    print(new_fen + ' ' + ''.join((c.upper() if c.islower() and c.lower() in ['k', 'q'] else c.lower() for c in meta)))