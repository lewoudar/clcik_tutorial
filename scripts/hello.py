"""A simple example to greet someone"""
import click


@click.command()
@click.option('-n', '--name', prompt='Your name', help='Name to greet')
def cli(name):
    """Greets a user who gives his name as input"""
    click.echo(f'Hello {name}!')
