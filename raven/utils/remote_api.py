# -*- coding: utf-8 -*-
from typing import Dict

import requests


class RavenOpenApi():

    def __init__(self, root_path, username, password, provider='db'):
        self.root_path = root_path
        self.username = username
        self.password = password
        self.provider = provider

    def list_room(self, page=0, page_size=4) -> str:
        api_url = f'{self.root_path}/room/?q=(page:{page},page_size:{page_size})'
        with requests.Session() as s:
            headers = self._load_auth_header(s)
            r = s.get(api_url, headers=headers)
            return r.content.decode()

    def _load_auth_header(self, s: requests.Session) -> Dict[str, str]:
        api_url = f'{self.root_path}/security/login'
        body = {'username': self.username, 'password': self.password, 'provider': self.provider}
        r = s.post(api_url, json=body)
        token = r.json()['access_token']
        return {'Authorization': f'Bearer {token}'}
