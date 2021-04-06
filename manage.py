# -*- coding: utf-8 -*-
import logging
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


if __name__ == '__main__':
    cli()
