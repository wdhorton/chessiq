import os

import berserk

LICHESS_TOKEN = os.getenv('LICHESS_TOKEN')

session = berserk.TokenSession(LICHESS_TOKEN)
client = berserk.Client(session=session)

def get_game(game_id):
    return client.games.export(game_id, as_pgn=True)

def get_study(study_id):
    return client.studies.export(study_id)