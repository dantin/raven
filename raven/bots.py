# -*- coding: utf-8 -*-

import logging
import json

from slixmpp import ClientXMPP

from raven.utils.codec import xml_unescape


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
            body = xml_unescape(msg['body'])
            logger.debug('unescaped mesage: %s', body)
            try:
                cmd = json.loads(body)
                if cmd and 'name' in cmd:
                    if 'rooms' == cmd['name']:
                        rooms = self.remote_api.list_room()
                        resp = rooms.decode()
                else:
                    resp = 'no name in command: %(body)s' % msg
            except Exception as e:
                resp = 'bad json'
                logger.warning(e)

            self.send_message(
                mto=msg['from'],
                mbody=resp,
                mtype=msg['type'],
            )
