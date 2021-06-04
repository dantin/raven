# -*- coding: utf-8 -*-
import pytest

from raven.utils.codec import xml_escape, xml_unescape, decode, RequestMessage, RequestType


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
    'body,expected',
    [
        ('{"cmd": "rooms", "page": 0, "page_size": 4}',
            RequestMessage(request_type=RequestType.LIST_ROOM, extra={'page': 0, 'page_size': 4})),
        ('{"cmd": "rooms"}',
            RequestMessage(request_type=RequestType.LIST_ROOM, extra={'page': 0, 'page_size': 4})),
        ('{"cmd": "xxx"}',
            RequestMessage(request_type=RequestType.UNKNOWN, extra=None)),
        ('{"xxx": "xxx"}',
            RequestMessage(request_type=RequestType.UNKNOWN, extra=None)),
    ],
)
def test_decode(body, expected):
    actual = decode(body)
    assert actual == expected
