# -*- coding: utf-8 -*-
import json
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional, Tuple
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


def parse_message(content: str) -> Tuple[bool, RequestMessage]:
    try:
        content = xml_unescape(content)
        print(content)
        elem = json.loads(content)
        if 'cmd' not in elem:
            return False, None

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
                    'room_id': elem.get('id', 0)})
        else:
            req = RequestMessage(
                request_type=RequestType.UNKNOWN,
                extra=None)

        return True, req
    except Exception as e:
        logger.warning(e)
        return False, None
