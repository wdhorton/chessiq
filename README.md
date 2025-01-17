# ChessIQ

Requires Python 3.8 or higher.

## Installation
```
git clone https://github.com/wdhorton/chessiq.git
cd chessiq
pip install .
```

## Basic usage

```
chessiq opening analyze-games --repertoire_pgn /path/to/repertoire.pgn --games_pgn /path/to/games.pgn
```

## API

The `chessiq` command currently has two subcommands: `opening` and `config`.

`opening`



`config`

You can use this to interact with the configuration of the tool. You can set defaults for these values:
```
"format",
"db_start_date",
"db_end_date", 
"db_time_controls",
"db_ratings",
"use_engine",
"engine_depth",
"engine_file",
"repertoire_pgn"
```

with `chessiq config set <name> <value>`.

You can also retrieve the current config values using `chessiq config get`.

## Lichess integration

The tool can download PGNs from Lichess for you, so it can also be run like this:
```
chessiq analyze-opening --study_id 12345678 --game_id 56789012
```

If you want to access a private Lichess study you will first need to [create a personal access token](https://lichess.org/account/oauth/token). Then make that token available by running:
```
$ export LICHESS_TOKEN="paste your token here"
```
