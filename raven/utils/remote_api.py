# -*- coding: utf-8 -*-
import json
import logging
from typing import Dict

from raven.utils.http import get, post


logger = logging.getLogger(__name__)


class RavenOpenApi():

    def __init__(self, root_path, username, password, provider='db'):
        self.root_path = root_path
        self.username = username
        self.password = password
        self.provider = provider

    def list_room(self, page=0, page_size=4) -> str:
        logger.debug(f'List rooms of page {page}, size {page_size}')

        api_url = f'{self.root_path}/room/?q=(page:{page},page_size:{page_size})'
        headers = self._load_auth_header()
        r = get(api_url, None, headers=headers)
        count = r['count']
        cols = r['list_columns']
        size = len(r['result'])
        records = []
        for i, row in zip(r['ids'], r['result']):
            record = {}
            for name in cols:
                record[name] = row[name]
                records.append(record)
        return json.dumps({'count': count, 'size': size, 'records': records})

    def get_room(self, room_id: int) -> str:
        logger.debug(f'Get room by id {room_id}')

        api_url = f'{self.root_path}/room/detail/{room_id}'
        headers = self._load_auth_header()
        r = get(api_url, None, headers=headers)
        return json.dumps(r)

    def profile(self, jabber_id: str) -> str:
        logger.debug(f'Get profile of {jabber_id}')

        api_url = f'{self.root_path}/security/{jabber_id}/roles'
        headers = self._load_auth_header()
        r = get(api_url, None, headers=headers)
        return json.dumps(r)

    def _load_auth_header(self) -> Dict[str, str]:
        api_url = f'{self.root_path}/security/login'
        body = {'username': self.username, 'password': self.password, 'provider': self.provider}
        r = post(api_url, json=body)
        token = r['access_token']
        return {'Authorization': f'Bearer {token}'}
