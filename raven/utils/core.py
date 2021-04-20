# -*- coding: utf-8 -*-
import os
from configparser import ConfigParser
from typing import Tuple

from sqlalchemy import event, exc, select
from sqlalchemy.engine import Connection, Engine

from raven.config import DATA_DIR


class RavenConfig():
    def __init__(self, filename=os.path.join(DATA_DIR, 'raven.cfg')):
        self.filename = filename
        cfg = ConfigParser()
        cfg.read(filename)
        self.cfg = cfg

    def update_api(self, root_path: str, username: str, password: str) -> None:
        if not self.cfg.has_section('api'):
            self.cfg.add_section('api')

        self.cfg.set('api', 'root_path', root_path)
        self.cfg.set('api', 'username', username)
        self.cfg.set('api', 'password', password)
        self._save()

    def update_jabber(self, nickname: str, username: str, password: str) -> None:
        if not self.cfg.has_section('jabber'):
            self.cfg.add_section('jabber')

        self.cfg.set('jabber', 'nickname', nickname)
        self.cfg.set('jabber', 'username', username)
        self.cfg.set('jabber', 'password', password)
        self._save()

    def load_api(self) -> Tuple[str, str, str]:
        root_path = self.cfg.get('api', 'root_path')
        username = self.cfg.get('api', 'username')
        password = self.cfg.get('api', 'password')
        return root_path, username, password

    def load_jabber(self) -> Tuple[str, str, str]:
        nickname = self.cfg.get('jabber', 'nickname')
        username = self.cfg.get('jabber', 'username')
        password = self.cfg.get('jabber', 'password')
        return nickname, username, password

    def _save(self):
        with open(self.filename, 'w') as f:
            self.cfg.write(f)


def pessimistic_connection_handling(some_engine: Engine) -> None:
    @event.listens_for(some_engine, 'engine_connect')
    def ping_connection(
        connection: Connection, branch: bool
    ) -> None:
        if branch:
            # 'branch' refer to a sub-connection of a connection
            # we don't want to bother pinging on these.
            return

        # turn off 'close with result'.  This flag is only used with
        # 'connectionless' execution, otherwise will be False in any case.
        save_should_close_with_result = connection.should_close_with_result
        connection.should_close_with_result = False

        try:
            # run a SELECT 1.   use a core select() so that
            # the SELECT of a scalar value without a table is
            # appropriately formatted for the backend.
            connection.scalar(select([1]))
        except exc.DBAPIError as err:
            # catch SQLAlchemy's DBAPIError, which is a wrapper
            # for the DBAPI's exception.  It includes a .connection_invalidated
            # attribute which specifies if this connection is a 'disconnect'
            # candition, which is based on inspection of the original exception
            # by the dialect in use.
            if err.connection_invalidated:
                # run the same SELECT again - the connection with re-validate
                # itself and establish a new connection.  The disconnect detection
                # here also causes the whole connection pool to be invalidated
                # so that all stale connection are discarded.
                connection.scalar(select[1])
            else:
                raise
        finally:
            # restore 'close with result'.
            connection.should_close_with_result = save_should_close_with_result
