# -*- coding: utf-8 -*-
import logging
import signal
from threading import Event
from typing import Any, Dict

import click
from colorama import Fore, Style
from flask.cli import FlaskGroup, with_appcontext

from raven import app, appbuilder, security_manager
from raven.app import create_app
from raven.extensions import db


logger = logging.getLogger(__name__)


def normalize_token(token_name: str) -> str:
    return token_name.replace('_', '-')


@click.group(
    cls=FlaskGroup,
    create_app=create_app,
    context_settings={'token_normalize_func': normalize_token},
)
@with_appcontext
def cli() -> None:
    """This is a management script for the Raven application."""
    @app.shell_context_processor
    def make_shell_context() -> Dict[str, Any]:
        return dict(app=app, db=db)


@cli.command()
@with_appcontext
@click.option('--api_root', '-a', help='API root path')
@click.option('--username', '-u', help='Jabber username')
@click.option('--password', '-p', help='Jabber password')
@click.option('--nickname', '-n', help='Jabber nickname')
def init(username: str, password: str, nickname: str, api_root: str) -> None:
    """Initialize the Raven application."""
    appbuilder.add_permissions(update_perms=True)
    security_manager.sync_role_definitions()


@cli.command()
@with_appcontext
@click.option('--root_path', default='http://127.0.0.1:8080/api/v1', prompt='API root path')
@click.option('--username', default='admin', prompt='API authenticate username')
@click.password_option()
def setup_api(root_path: str, username: str, password: str) -> None:
    """Setup the Raven API configuration."""
    from raven.config import RavenConfig

    cfg = RavenConfig()
    cfg.update_api(root_path, username, password)
    click.echo(click.style('API User {0} updated.'.format(username), fg='green'))


@cli.command()
@with_appcontext
@click.option('--nickname', default='nickname', prompt='Jabber nickname')
@click.option('--username', default='user@localhost', prompt='Jabber username')
@click.password_option()
def setup_jabber(nickname, username, password) -> None:
    """Setup the Raven Jabber configuration."""
    from raven.config import RavenConfig

    cfg = RavenConfig()
    cfg.update_jabber(nickname, username, password)
    click.echo(click.style('Jabber User {0} updated.'.format(username), fg='green'))


@cli.command()
@with_appcontext
@click.option('--verbose', '-v', is_flag=True, help='Show extra information')
def version(verbose: bool) -> None:
    """Prints the current version number"""
    print(Fore.BLUE + '==' * 15)
    print(
        Fore.YELLOW + 'Raven ' + Fore.CYAN + '0.1-dev'
    )
    print(Fore.BLUE + '==' * 15)
    if verbose:
        print(f'[DB]: {db.engine}')
    print(Style.RESET_ALL)


@cli.command()
@with_appcontext
def bot() -> None:
    """Run XMPP Robot Client."""

    from raven.bots import UltrasoundBot
    from raven.config import RavenConfig
    from raven.remote.client import RavenOpenApi

    cfg = RavenConfig()
    nickname, username, password = cfg.load_jabber()
    click.echo(click.style('Jabber Bot {0} prepare to login.'.format(nickname), fg='green'))

    def shutdown_cb(sig, frame):
        """Callback function for shutdown event."""
        logger.info('Recieve signal #%d, shutdown...', sig)
        _shutdown_event.set()

    # shutdown event
    _shutdown_event = Event()
    # Register shutdown handler.
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, shutdown_cb)

    root_path, api_username, api_password = cfg.load_api()
    remote_api = RavenOpenApi(root_path, api_username, api_password)
    xmpp = UltrasoundBot(username, password, nickname, remote_api)
    xmpp.register_plugin('xep_0030')  # Service Discovery
    xmpp.register_plugin('xep_0045')  # Multi-User Chat
    xmpp.register_plugin('xep_0085')  # Chat State Notification
    xmpp.register_plugin('xep_0092')  # Software Version
    xmpp.register_plugin('xep_0199')  # XMPP Ping

    xmpp.connect()
    click.echo(click.style('Jabber Bot {0} connected.'.format(nickname), fg='green'))

    while not _shutdown_event.is_set():
        xmpp.process(timeout=1.0)
    xmpp.disconnect()
    click.echo(click.style('Jabber Bot {0} disconnected.'.format(nickname), fg='green'))


if __name__ == '__main__':
    cli()
