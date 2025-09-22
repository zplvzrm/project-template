"""Command line"""
import click
from click import Context

from project_template import __version__
from project_template.config import settings
from project_template.log import init_log
from project_template.manage import Manage
from project_template.example_blog.server import Server


@click.group(invoke_without_command=True)
@click.pass_context
@click.option(
    '-V',
    '--version',
    is_flag=True,
    help='Show version and exit.'
)  # If it's true, it will override `settings.VERBOSE`
@click.option('-v', '--verbose', is_flag=True, help='Show more info.')
@click.option(
    '--debug',
    is_flag=True,
    help='Enable debug.'
)  # If it's true, it will override `settings.DEBUG`
def main(ctx: Context, version: str, verbose: bool, debug: bool):
    """Main commands"""
    if version:
        click.echo(__version__)
    elif ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
    else:
        if verbose:
            settings.set('VERBOSE', True)
        if debug:
            settings.set('DEBUG', True)


@main.command()
@click.option('-h', '--host', show_default=True, help=f'Host IP. Default: {settings.HOST}')
@click.option('-p', '--port', show_default=True, type=int, help=f'Port. Default: {settings.PORT}')
@click.option('--level', help='Log level')
def server(host, port, level):
    """Start server."""
    kwargs = {
        'LOGLEVEL': level,
        'HOST': host,
        'PORT': port,
    }
    for name, value in kwargs.items():
        if value:
            settings.set(name, value)

    Server().run()
    
@main.command()
def run():
    """Run command"""
    init_log()
    manage = Manage()
    manage.run()
    