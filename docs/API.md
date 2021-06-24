# API

This document describe API for chatbot.

### List Rooms

    {"cmd": "rooms", "page": 0, "page_size": 1}

Details:

1. `cmd`: name of the command, should be `rooms`;
2. `page`: page numbers, optional;
3. `page_size`: page size, optional;

### Get Room

    {"cmd": "room", "jabber-id": "room02@conference.localhost"}

Details:

1. `cmd`: name of the command, should be `room`;
2. `jabber-id`: room jabber id;

### Profile

    {"cmd": "profile"}

Details:

1. `cmd`: name of the command, should be `profile`;
