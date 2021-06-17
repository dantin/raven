# -*- coding: utf-8 -*-
import logging

from flask import Response
from flask_appbuilder.api import expose, protect, safe
from flask_appbuilder.models.sqla.interface import SQLAInterface

from raven.models import Room
from raven.videos.dao import RoomDAO
from raven.views.base_api import BaseRavenModelRestApi


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

    @expose('/detail/<jabber_id>', methods=['GET'])
    @protect()
    @safe
    def get(self, jabber_id: int) -> Response:
        logger.debug(f'get room info by {jabber_id}')

        room = RoomDAO.get_by_jabber_id(jabber_id)
        streams = []
        for box in room.video_boxes:
            streams.extend([{
                'type': video_stream.stream_type,
                'push_url': video_stream.push_url,
                'broadcast_url': video_stream.broadcast_url,
            } for video_stream in box.video_streams])
        return self.response(200, result={
            'id': room.id,
            'name': room.name,
            'jabber_id': room.jabber_id,
            'streams': streams,
        })
