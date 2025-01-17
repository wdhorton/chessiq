from pathlib import Path
import time
import yaml


DEFAULT_CONFIG_FILE = Path("~/.chessiq/config.yaml").expanduser()
DEFAULT_CONFIG_FILE.parent.mkdir(exist_ok=True, parents=True)
DEFAULT_CONFIG_FILE.touch()

CONFIG_KEYS = [
    "format",
    "db_start_date",
    "db_end_date", 
    "db_time_controls",
    "db_ratings",
    "use_engine",
    "engine_depth",
    "engine_file",
    "repertoire_pgn"
]

def set_config_value(key, value):
    with DEFAULT_CONFIG_FILE.open() as f:
        config = yaml.safe_load(f) or {}

    config[key] = value

    with DEFAULT_CONFIG_FILE.open("w") as f:
        yaml.dump(config, f)


def set_config_value_interactive():
    pass


DEFAULTS = {
    "format": "json",
    "db_start_date": "2012-01",
    "db_end_date": time.strftime("%Y-%m"),
    "db_time_controls": "blitz,rapid,classical",
    "db_ratings": "1600,1800,2000,2200,2500",
}


def get_config(key):
    with DEFAULT_CONFIG_FILE.open() as f:
        config = yaml.safe_load(f) or {}

    if key is None:
        return config

    return config.get(key, DEFAULTS.get(key))