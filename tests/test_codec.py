# -*- coding: utf-8 -*-
import pytest

from raven.utils.codec import xml_escape, xml_unescape


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
