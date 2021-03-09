# -*- coding: utf-8 -*-
import click

from setting import VERSION

CONTEXT_SETTINGS = {'help_option_names': ['-h', '--help']}


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=VERSION)
def cli():
    """Raven CLI utilities."""
    pass


@cli.command(name='server')
def server():
    """Run API Server."""
    click.echo(f'VERSION: {VERSION}\n')

    from api import run_api_server
    listen_addr = '0.0.0.0:9527'
    run_api_server(listen_addr)


@cli.command(name='robot')
def robot():
    """Run XMPP Bot Service."""
    click.echo(f'VERSION: {VERSION}\n')


if __name__ == '__main__':
    cli()
