# -*- coding: utf-8 -*-

import requests


class RavenOpenApi():

    def __init__(self, root_path, username, password, provider='db'):
        self.root_path = root_path
        self.username = username
        self.password = password
        self.provider = provider

    def list_room(self, page=0, page_size=4):
        url_path = f'{self.root_path}/room/?q(page:{page},page_size:{page_size})'
        r = requests.get(url_path, headers=self._load_auth_header())
        return r.content

    def _load_auth_header(self):
        url_path = f'{self.root_path}/security/login'
        body = {'username': self.username, 'password': self.password, 'provider': self.provider}
        r = requests.post(url_path, json=body)
        token = r.json()['access_token']
        return {'Authorization': f'Bearer {token}'}
