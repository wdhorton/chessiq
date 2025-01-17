import click

from chessiq.opening_analyzer.command import opening
from chessiq.config_manager.command import config


@click.group()
def cli():
    pass

cli.add_command(opening)
cli.add_command(config)


if __name__ == '__main__':
    cli()