"""A simple implementation of an http client"""
from typing import Tuple, Dict, List, Optional

import click
import httpx

from .http_util import print_http_response


class RequestData:
    def __init__(self, verify: bool):
        self.verify = verify


def parse_value(value: str) -> Tuple[str, str]:
    parts = value.split(':')
    if len(parts) != 2 or not parts[1]:
        raise click.UsageError(f'parameter "{value}" is not in the form key:value')
    return parts[0], parts[1]


def get_dict_value(items: List[str]) -> Dict[str, str]:
    result = {}
    for item in items:
        key, value = parse_value(item)
        result[key] = value
    return result


HTTPProperty = Optional[Dict[str, str]]


def get_http_arguments(
        query: List[str] = None,
        headers: List[str] = None,
        cookies: List[str] = None,
        form: List[str] = None,
        json_data: List[str] = None,
) -> Tuple[HTTPProperty, HTTPProperty, HTTPProperty, HTTPProperty, HTTPProperty]:
    cookies = get_dict_value(cookies) if cookies is not None else cookies
    headers = get_dict_value(headers) if headers is not None else headers
    query = get_dict_value(query) if query is not None else query
    form = get_dict_value(form) if form is not None else form
    json_data = get_dict_value(json_data) if json_data is not None else json_data
    return cookies, headers, query, form, json_data


@click.group()
@click.option('--verify/--no-verify', default=True, help='Check the TLS certificate')
@click.pass_context
def cli(context, verify):
    """A simple HTTP client"""
    context.obj = RequestData(verify)


@cli.command()
@click.option('-q', '--query', multiple=True, help='query string parameter')
@click.option('-H', '--headers', multiple=True, help='HTTP header')
@click.option('-c', '--cookies', multiple=True, help='HTTP cookie')
@click.argument('url')
@click.pass_obj
def get(obj, url, cookies, headers, query):
    """Performs an HTTP GET request given an URL"""
    cookies, headers, query, *_ = get_http_arguments(cookies=cookies, query=query, headers=headers)
    response = httpx.get(url, verify=obj.verify, params=query, headers=headers, cookies=cookies)
    print_http_response(response)


@cli.command()
@click.option('-q', '--query', multiple=True, help='query string parameter')
@click.option('-H', '--headers', multiple=True, help='HTTP header')
@click.option('-c', '--cookies', multiple=True, help='HTTP cookie')
@click.option('-f', '--form', multiple=True, help='HTTP form data')
@click.option('-j', '--json', 'json_data', multiple=True, help='HTTP JSON data')
@click.argument('url')
@click.pass_obj
def post(obj, url, cookies, headers, query, form, json_data):
    """Performs an HTTP POST request given an URL"""
    cookies, headers, query, form, json_data = get_http_arguments(
        query, headers, cookies, form, json_data
    )
    response = httpx.post(
        url, verify=obj.verify, params=query, cookies=cookies, headers=headers,
        data=form, json=json_data
    )
    print_http_response(response)
