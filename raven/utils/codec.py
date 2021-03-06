# -*- coding: utf-8 -*-
import json
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional
from xml.sax.saxutils import escape, unescape


logger = logging.getLogger(__name__)
__xml_escape_table__ = {
    '"': '&quot;',
    "'": '&apos;',
}
__xml_unescape_table__ = {v: k for k, v in __xml_escape_table__.items()}


def xml_escape(s: str) -> str:
    return escape(s, __xml_escape_table__)


def xml_unescape(s: str) -> str:
    return unescape(s, __xml_unescape_table__)


class RequestType(str, Enum):
    """
    Types of request that can handled by Raven.
    """
    LIST_ROOM = 'rooms'
    PROFILE = 'profile'
    GET_ROOM = 'room'
    UNKNOWN = 'unkonwn'


@dataclass
class RequestMessage():
    """
    A message that is requested from client.
    """
    request_type: RequestType
    extra: Optional[Dict[str, Any]] = None


def decode(content: str) -> RequestMessage:
    try:
        content = xml_unescape(content)
        elem = json.loads(content)
        if 'cmd' not in elem:
            return RequestMessage(
                request_type=RequestType.UNKNOWN,
                extra=None)

        cmd = elem['cmd']
        if cmd == 'rooms':
            req = RequestMessage(
                request_type=RequestType.LIST_ROOM,
                extra={
                    'page': elem.get('page', 0),
                    'page_size': elem.get('page_size', 4)})
        elif cmd == 'profile':
            req = RequestMessage(
                request_type=RequestType.PROFILE,
                extra=None)
        elif cmd == 'room':
            req = RequestMessage(
                request_type=RequestType.GET_ROOM,
                extra={
                    'jabber-id': elem.get('jabber-id', '')})
            print(elem.get('jabber-id', ''))
        else:
            req = RequestMessage(
                request_type=RequestType.UNKNOWN,
                extra=None)

        return req
    except Exception as e:
        logger.warning(e)
        return RequestMessage(
            request_type=RequestType.UNKNOWN,
            extra=None)


def encode(entity: Any) -> str:
    return json.dumps(entity)
