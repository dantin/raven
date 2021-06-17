# -*- coding: utf-8 -*-
import logging
from typing import Any, Dict

from slixmpp.jid import JID

from raven.exceptions import RemoteAPIError
from raven.utils.http import get, post
from raven.config import RavenAPIConfig, RavenJabberAPIConfig


logger = logging.getLogger(__name__)


class RavenOpenApi():

    def __init__(self, provider: str = 'db'):
        cfg = RavenAPIConfig()
        self.root_path = cfg.root_path
        self.username = cfg.username
        self.password = cfg.password
        self.provider = provider

    def list_room(self, page=0, page_size=4) -> Dict[str, Any]:
        logger.debug(f'list rooms of page {page}, size {page_size}')

        api_url = f'{self.root_path}/room/?q=(page:{page},page_size:{page_size})'
        try:
            headers = self._load_auth_header()
            r = get(api_url, None, headers=headers)
            count = r['count']
            result = r['result']
            records = []
            for row in result:
                room_id = row['id']
                room = self.get_room(room_id)
                if not room:
                    continue
                records.append(room)
            return {'result': {'count': count, 'size': len(result), 'records': records}}
        except RemoteAPIError:
            logger.warn(f'fail to list room of page {page}, size {page_size}')
            return {}

    def get_room(self, jabber_id: str) -> Dict[str, Any]:
        logger.debug(f'get room by {jabber_id}')

        api_url = f'{self.root_path}/room/detail/{jabber_id}'
        try:
            headers = self._load_auth_header()
            return get(api_url, None, headers=headers)
        except RemoteAPIError:
            logger.warn(f'fail to get room by {jabber_id}')
            return {}

    def profile(self, jabber_id: str) -> Dict[str, Any]:
        logger.debug(f'get profile of {jabber_id}')

        api_url = f'{self.root_path}/security/{jabber_id}/roles'
        try:
            headers = self._load_auth_header()
            return get(api_url, None, headers=headers)
        except RemoteAPIError:
            logger.warn(f'fail to get profile of {jabber_id}')
            return {}

    def _load_auth_header(self) -> Dict[str, str]:
        api_url = f'{self.root_path}/security/login'
        body = {'username': self.username, 'password': self.password, 'provider': self.provider}
        r = post(api_url, json=body)
        token = r['access_token']
        return {'Authorization': f'Bearer {token}'}


class EjabberdOpenAPI():

    def __init__(self) -> None:
        cfg = RavenJabberAPIConfig()
        self.root_path = cfg.root_path
        self.username = cfg.username
        self.password = cfg.password

    def check_account(self, jabber_id: str) -> bool:
        """check if an account exists or not."""
        logger.debug(f'check if account {jabber_id} exists or not')

        api_url = f'{self.root_path}/api/check_account'
        jid = JID(jabber_id)
        body = {'user': jid.user, 'host': jid.host}
        try:
            return post(api_url, json=body) == 0
        except RemoteAPIError:
            return False

    def register(self, jabber_id: str, password: str = 'password') -> bool:
        """register a user."""
        logger.debug(f'register account {jabber_id}')

        api_url = f'{self.root_path}/api/register'
        jid = JID(jabber_id)
        body = {'user': jid.user, 'host': jid.host, 'password': password}
        try:
            post(api_url, json=body)
            return True
        except RemoteAPIError:
            return False

    def unregister(self, jabber_id: str) -> bool:
        """unregister a user."""
        logger.debug(f'unregister account {jabber_id}')

        api_url = f'{self.root_path}/api/unregister'
        jid = JID(jabber_id)
        body = {'user': jid.user, 'host': jid.host}
        try:
            post(api_url, json=body)
            return True
        except RemoteAPIError:
            return False

    def create_room(self, jabber_id: str, host: str = 'localhost', **kwargs) -> bool:
        """create a MUC room in host with given options."""
        logger.debug(f'create a MUC room using {jabber_id}')

        api_url = f'{self.root_path}/api/create_room_with_opts'
        jid = JID(jabber_id)
        options = [{'name': k, 'value': v} for k, v in kwargs.items()]
        body = {'name': jid.user, 'service': jid.host, 'host': host, 'options': options}
        try:
            post(api_url, json=body)
            return True
        except RemoteAPIError:
            return False

    def destroy_room(self, jabber_id: str) -> bool:
        """destroy a MUC room."""
        logger.debug(f'destroy a MUC room by {jabber_id}')

        api_url = f'{self.root_path}/api/destroy_room'
        jid = JID(jabber_id)
        body = {'name': jid.user, 'service': jid.host}
        try:
            post(api_url, json=body)
            return True
        except RemoteAPIError:
            return False

    def check_room(self, jabber_id: str) -> bool:
        """check if a room exists or not."""
        logger.debug(f'check if room {jabber_id} exists or not')

        api_url = f'{self.root_path}/api/get_room_options'
        jid = JID(jabber_id)
        body = {'name': jid.user, 'service': jid.host}
        try:
            props = post(api_url, json=body)
            return len(props) > 0
        except RemoteAPIError:
            return False
