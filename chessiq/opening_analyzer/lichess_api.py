import os

import berserk
import requests


DB_URL = "https://explorer.lichess.ovh/lichess"

LICHESS_TOKEN = os.getenv('LICHESS_TOKEN')

if LICHESS_TOKEN:
    session = berserk.TokenSession(LICHESS_TOKEN)
else:
    session = None

client = berserk.Client(session=session)


def get_game(game_id):
    return client.games.export(game_id, as_pgn=True)

def get_study(study_id):
    return client.studies.export(study_id)

def get_position(board, db_start_date, db_end_date, time_controls, ratings):
    response = requests.get(DB_URL, params={
        "variant": "standard",
        "fen": board.fen(),
        "since": db_start_date,
        "until": db_end_date,
        "speeds": time_controls,
        "ratings": ratings,
    })
    return response.json()

def get_frequency_of_position(board, db_start_date, db_end_date, time_controls, ratings):
    response_dict = get_position(board, db_start_date, db_end_date, time_controls, ratings)
    return response_dict["white"] + response_dict["draws"] + response_dict["black"]


def get_moves_at_position(board, db_start_date, db_end_date, time_controls, ratings):
    response_dict = get_position(board, db_start_date, db_end_date, time_controls, ratings)
    return response_dict["moves"]

def get_latest_game(username):
    return next(client.games.export_by_player(username, max=1, as_pgn=True))