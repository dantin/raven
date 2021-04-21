# -*- coding: utf-8 -*-
import pytest

from raven.utils.codec import xml_escape, xml_unescape, parse_message, RequestMessage, RequestType


@pytest.mark.parametrize(
    'content,expected',
    [
        ('"', '&quot;'),
        ("'", '&apos;'),
    ],
)
def test_xml_escape(content, expected):
    actual = xml_escape(content)
    assert actual == expected


@pytest.mark.parametrize(
    'content,expected',
    [
        ('&quot;', '"'),
        ('&apos;', "'"),
    ],
)
def test_xml_unescape(content, expected):
    actual = xml_unescape(content)
    assert actual == expected


@pytest.mark.parametrize(
    'body,is_ok,expected',
    [
        ('{"cmd": "rooms", "page": 0, "page_size": 4}', True,
            RequestMessage(request_type=RequestType.LIST_ROOM, extra={'page': 0, 'page_size': 4})),
        ('{"cmd": "rooms"}', True,
            RequestMessage(request_type=RequestType.LIST_ROOM, extra={'page': 0, 'page_size': 4})),
        ('{"cmd": "xxx"}', True,
            RequestMessage(request_type=RequestType.UNKNOWN, extra=None)),
        ('{"xxx": "xxx"}', False, None),
    ],
)
def test_parse_message(body, is_ok, expected):
    ok, actual = parse_message(body)
    assert ok == is_ok
    assert actual == expected
