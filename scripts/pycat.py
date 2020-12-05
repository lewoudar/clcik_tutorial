"""An example simulating the cat unix command"""
import click


@click.command()
@click.option('-n', 'print_line', is_flag=True,
              help='print the line number next to the line if specified')
@click.argument('file', type=click.File())
def cli(file, print_line):
    """FILE represents the path to a file on the system"""
    if print_line:
        count = 1
        for line in file:
            click.echo(f'{count} {line}', nl=False)
            count += 1
    else:
        click.echo(file.read())
