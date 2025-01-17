from chess import BLACK


import chess

from chessiq.opening_analyzer.lichess_api import get_moves_at_position

seed = "1.e4 c5 2. Nf3 d6 3. d4 cxd4"
seed_moves = list(seed)

# This is a BFS

# map of positions to moves?
visited = {}

# map of position to set move
seed_moves = {

}

children = {}

THRESHOLD_PERCENTILE = 0.95

SIDE = BLACK

board = chess.Board()

queue = []
board.push(seed_moves[0])
queue.append(board)

while queue:

    position = queue.pop(0)

    moves = get_moves_at_position()
    # if the player to move is SIDE then check the seed moves, 
    # if not there then take most frequent master move (add in engine move as well?)

    # else take all the candidate moves from the lichess DB
    total = sum() #move counts
    running_percentile = 0
    i = 0
    while running_percentile < THRESHOLD_PERCENTILE:
        move = moves[i]
        running_percentile += move_freq / total
        # probably want to copy the board here
        position.push(move)
        if not visited[position]:
            queue.push(position)
            visited[position] = True
            # if you're going depth first can you just add to the same game with variations? each representation could just be a string of moves from the beginning, keep adding to the game
            children[old_position] = new_position


board = chess.Board()
board.push(seed_moves[0])

moves = children[board]



