# -*- coding: utf-8 -*-
import logging
from typing import Any, Dict

import requests

from raven.exceptions import RemoteAPIError


logger = logging.getLogger(__name__)


def get(url: str, params: Dict[str, Any], headers: Dict[str, Any]) -> Any:
    """get send HTTP GET request."""
    logger.debug(f'GET from "{url}"')
    with requests.Session() as s:
        resp = s.get(url, params=params, headers=headers)
        if resp.status_code != 200:
            raise RemoteAPIError('fail to get information')
        return resp.json()


def post(url: str, json: Dict[str, Any]) -> Any:
    """post send HTTP POST in JSON."""
    logger.debug(f'POST to "{url}"')
    with requests.Session() as s:
        resp = s.post(url, json=json)
        if resp.status_code != 200:
            raise RemoteAPIError('fail to post information')
        return resp.json()
