import json

import click

from chessiq.config_manager.config import set_config_value, get_config

@click.group()
def config():
    pass

@config.command()
@click.argument("key")
@click.argument("val")
def set(key, val):
    set_config_value(key, val)

@config.command()
@click.argument("key")
def get(key):
    print(json.dumps(get_config(key), indent=4))