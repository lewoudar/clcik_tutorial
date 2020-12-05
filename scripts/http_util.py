"""Helper function for http CLI"""
import click
import httpx
from pygments.formatters import get_formatter_by_name
from pygments.lexers import get_lexer_by_name
from pygments import highlight


def print_http_response(response: httpx.Response) -> None:
    result = f'{response.http_version} {response.status_code} {response.reason_phrase}\n'
    for key, value in response.headers.items():
        result += f'{key.title()}: {value}\n'
    result += f'\n{response.text}'

    http_lexer = get_lexer_by_name('http')
    console = get_formatter_by_name('console')
    click.echo(highlight(result, http_lexer, console))
