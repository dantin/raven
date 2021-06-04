# -*- coding: utf-8 -*-
import logging

from flask import Response
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.api import expose, protect, safe

from raven.views.base_api import BaseRavenModelRestApi
from raven.videos.dao import RoomDAO
from raven.models import Room


logger = logging.getLogger(__name__)


class RoomRestApi(BaseRavenModelRestApi):
    datamodel = SQLAInterface(Room)
    resource_name = 'room'

    class_permission_name = 'Room'

    list_columns = [
        'id',
        'name',
        'jabber_id',
    ]

    show_columns = [
        'id',
        'name',
        'jabber_id',
    ]

    @expose('/detail/<room_id>', methods=['GET'])
    @protect()
    @safe
    def get(self, room_id: int) -> Response:
        logger.debug(f'get room info with {room_id}')

        room = RoomDAO.get_by_id(room_id)
        streams = []
        for box in room.video_boxes:
            streams.extend([{
                'type': video_stream.stream_type,
                'push_url': video_stream.push_url,
                'broadcast_url': video_stream.broadcast_url,
            } for video_stream in box.video_streams])
        return self.response(200, result={
            'id': room_id,
            'name': room.name,
            'jabber_id': room.jabber_id,
            'streams': streams,
        })
