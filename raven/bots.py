# -*- coding: utf-8 -*-
import logging

from slixmpp import ClientXMPP
from slixmpp.jid import JID

from raven.utils.codec import decode, encode, RequestType
from raven.remote.client import RavenOpenApi
from raven.config import RavenJabberConfig


logger = logging.getLogger(__name__)


class UltrasoundBot(ClientXMPP):
    def __init__(self, cfg: RavenJabberConfig):
        ClientXMPP.__init__(self, cfg.username, cfg.password)
        self.use_message_ids = True
        self.use_ssl = True

        self.rooms = None
        self.nick = cfg.nickname
        self.remote_api = RavenOpenApi()

        # session start disconnect events.
        self.add_event_handler('session_start', self.start_session)
        # register receive handler for both groupchat and normal message events.
        self.add_event_handler('message', self.message)

    async def start_session(self, event) -> None:
        """session start."""
        await self.get_roster()
        self.send_presence()
        # self.join_rooms()

    def join_rooms(self) -> None:
        """method to join configured rooms and register their response handler"""
        if self.rooms:
            for room in self.rooms:
                # self.add_event_handler(f'muc::{room}::got_online', self.notify_user)
                self.plugin['xep_0045'].join_muc(room, self.nick, wait=True)

    def message(self, msg) -> None:
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
        req = decode(content)

        if req.request_type == RequestType.LIST_ROOM:
            page, page_size = req.extra['page'], req.extra['page_size']
            resp = self.remote_api.list_room(page, page_size)
            reply = {
                'code': 0,
                'cmd': 'rooms',
                'page': page,
                'page_size': page_size,
                'result': resp['result'],
            }
        elif req.request_type == RequestType.PROFILE:
            resp = self.remote_api.profile(jabber_id.bare)
            reply = {
                'code': 0,
                'cmd': 'profile',
                'result': resp['result'],
            }
        elif req.request_type == RequestType.GET_ROOM:
            resp = self.remote_api.get_room(jabber_id=jabber_id.bare)
            reply = {
                'code': 0,
                'cmd': 'room',
                'result': resp['result'],
            }
        else:
            reply = {'code': 1, 'message': 'bad message format or type'}

        return encode(reply)
