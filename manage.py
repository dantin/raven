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
def init() -> None:
    """Initialize the Raven application."""
    appbuilder.add_permissions(update_perms=True)
    security_manager.sync_role_definitions()


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
    from raven.config import RavenJabberConfig

    cfg = RavenJabberConfig()
    click.echo(click.style(f'Jabber Bot {cfg.nickname} prepare to login.', fg='green'))

    def shutdown_cb(sig, frame):
        """Callback function for shutdown event."""
        logger.info('Recieve signal #%d, shutdown...', sig)
        _shutdown_event.set()

    # shutdown event
    _shutdown_event = Event()
    # Register shutdown handler.
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, shutdown_cb)

    xmpp = UltrasoundBot(cfg)
    xmpp.register_plugin('xep_0030')  # Service Discovery
    xmpp.register_plugin('xep_0045')  # Multi-User Chat
    xmpp.register_plugin('xep_0085')  # Chat State Notification
    xmpp.register_plugin('xep_0092')  # Software Version
    xmpp.register_plugin('xep_0199')  # XMPP Ping

    xmpp.connect()
    click.echo(click.style(f'Jabber Bot {cfg.nickname} connected.', fg='green'))

    while not _shutdown_event.is_set():
        xmpp.process(timeout=1.0)
    xmpp.disconnect()
    click.echo(click.style(f'Jabber Bot {cfg.nickname} disconnected.', fg='green'))


if __name__ == '__main__':
    cli()
