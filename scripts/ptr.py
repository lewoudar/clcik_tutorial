"""An example of implementation of custom parameter and its usage"""
import ipaddress
import click


class IPParamType(click.ParamType):
    name = 'ip address'

    def convert(self, value, param, ctx):
        try:
            return ipaddress.ip_address(value)
        except ValueError:
            self.fail(f'{value} is not a valid ip address', param, ctx)


@click.command()
@click.argument('ip_address', type=IPParamType())
def cli(ip_address):
    """Returns the PTR name of a given IP_ADDRESS"""
    click.echo(ip_address.reverse_pointer)
