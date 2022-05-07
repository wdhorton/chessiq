# ChessIQ

Requires Python 3.7 or higher.

## Installation
```
git clone https://github.com/wdhorton/chessiq.git
pip install .
```

## Basic usage

```
chessiq analyze-opening --repertoire_pgn /path/to/repertoire.pgn --games_pgn /path/to/games.pgn
```

## Lichess integration

The tool can download PGNs from Lichess for you, so it can also be run like this:
```
chessiq analyze-opening --study_id 12345678 --game_id 56789012
```

If you want to access a private Lichess study you will first need to [create a personal access token](https://lichess.org/account/oauth/token). Then make that token available by running:
```
$ export LICHESS_TOKEN="paste your token here"
```