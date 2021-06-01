# -*- coding: utf-8 -*-
import logging

from slixmpp import ClientXMPP
from slixmpp.jid import JID

from raven.utils.codec import parse_message, RequestType


logger = logging.getLogger(__name__)


class UltrasoundBot(ClientXMPP):
    def __init__(self, jid, password, nick, remote_api):
        ClientXMPP.__init__(self, jid, password)
        self.use_message_ids = True
        self.use_ssl = True

        self.rooms = None
        self.nick = nick
        self.remote_api = remote_api

        # session start disconnect events.
        self.add_event_handler('session_start', self.start_session)
        # register receive handler for both groupchat and normal message events.
        self.add_event_handler('message', self.message)

    async def start_session(self, event):
        """session start."""
        await self.get_roster()
        self.send_presence()
        # self.join_rooms()

    def join_rooms(self):
        """method to join configured rooms and register their response handler"""
        if self.rooms:
            for room in self.rooms:
                # self.add_event_handler(f'muc::{room}::got_online', self.notify_user)
                self.plugin['xep_0045'].join_muc(room, self.nick, wait=True)

    def message(self, msg):
        """
        method to handle incoming chat, normal messages
        :param msg: incoming msg object
        """
        # do not process our own messages
        # ourself = self.plugin["xep_0045"].get_our_jid_in_room(msg.get_mucroom())
        # if msg["from"] == ourself:
        #    return
        logger.debug('original message: %s', msg)

        # ever other messages will be answered statically
        if msg['type'] in ('normal', 'chat'):
            reply = self.process_message(msg['from'], msg['body'])

            self.send_message(
                mto=msg['from'],
                mbody=reply,
                mtype=msg['type'],
            )

    def process_message(self, jabber_id: JID, content: str) -> str:
        ok, req = parse_message(content)

        if not ok:
            return '{"code": 1, "message": "bad message format or type"}'

        if req.request_type == RequestType.LIST_ROOM:
            page, page_size = req.extra['page'], req.extra['page_size']
            reply = self.remote_api.list_room(page, page_size)
        elif req.request_type == RequestType.PROFILE:
            reply = self.remote_api.profile(jabber_id.bare)
        elif req.request_type == RequestType.GET_ROOM:
            room_id = req.extra['room_id']
            reply = self.remote_api.get_room(room_id)
        else:
            reply = '{"code": 1, "message": "unprocess"}'

        return reply
