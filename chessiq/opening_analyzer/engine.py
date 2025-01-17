import chess
import chess.engine

DEFAULT_DEPTH = 10

def analyze_position(board, multipv=1, depth=DEFAULT_DEPTH):
    engine = chess.engine.SimpleEngine.popen_uci("/usr/local/bin/stockfish")
    
    info = engine.analyse(board, chess.engine.Limit(depth=depth), multipv=multipv)
    if multipv == 1:
        result = info[0]['score'].relative.score()
    else:
        result = [(i['score'].relative.score(), i['pv']) for i in info]

    engine.quit()
    return result