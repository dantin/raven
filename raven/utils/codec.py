# -*- coding: utf-8 -*-

from xml.sax.saxutils import escape, unescape


__xml_escape_table__ = {
    '"': '&quot;',
    "'": '&apos;',
}
__xml_unescape_table__ = {v: k for k, v in __xml_escape_table__.items()}


def xml_escape(s: str) -> str:
    return escape(s, __xml_escape_table__)


def xml_unescape(s: str) -> str:
    return unescape(s, __xml_unescape_table__)
