"""An example simulating the less command"""
import click


@click.command()
@click.argument('file', type=click.File())
def cli(file):
    """Read file part by part"""
    click.echo_via_pager(file.read())
