from chessdotcom import get_player_game_archives, get_player_games_by_month

def get_game(game_id, username):
    response = get_player_game_archives(username)
    for archive in reversed(response.archives):
        response2 = get_player_games_by_month(username, archive.split("/")[-2], archive.split("/")[-1])
        for game in response2.games:
            if game_id in game.url:
                return game.pgn
