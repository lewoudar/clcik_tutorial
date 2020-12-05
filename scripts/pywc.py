"""An example simulating the wc command"""
import re
import click


@click.command()
@click.option('-m', 'chars', is_flag=True, help='number of characters')
@click.option('-l', 'lines', is_flag=True, help='number of lines')
@click.option('-c', 'byte', is_flag=True, help='number of bytes')
@click.option('-w', 'words', is_flag=True, help='number of words')
@click.argument('filename', type=click.Path(exists=True, dir_okay=False))
def cli(filename, words, byte, lines, chars):
    """Print newline, word, and byte counts for each file"""
    number_of_lines = 0
    file_content = ''
    number_of_words = 0
    with click.open_file(filename) as f:
        for line in f:
            file_content += line
            # line count
            number_of_lines += 1
            # word count
            line = line.strip(' \n')
            if not line:
                continue

            number_of_words += len(re.split(r'\s+', line))

    if not any([words, byte, lines, chars]):
        byte_length = len(file_content.encode())
        click.echo(f' {number_of_lines} {number_of_words} {byte_length} {filename}')
        return

    result = ''
    if lines:
        result += f' {number_of_lines}'
    if words:
        result += f' {number_of_words}'
    if byte:
        result += f' {len(file_content.encode())}'
    if chars:
        result += f' {len(file_content)}'
    result += f' {filename}'

    click.echo(result)
