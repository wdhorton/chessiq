import click

from chessiq.opening_analyzer.command import analyze_opening


@click.group()
def cli():
    pass

cli.add_command(analyze_opening)


if __name__ == '__main__':
    cli()