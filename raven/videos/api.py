# -*- coding: utf-8 -*-
import logging

from flask import Response
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.api import expose, protect, safe

from raven.views.base_api import BaseRavenModelRestApi
from raven.videos.dao import RoomDAO, VideoBoxDAO, VideoStreamDAO
from raven.models import Room


logger = logging.getLogger(__name__)


class RoomRestApi(BaseRavenModelRestApi):
    datamodel = SQLAInterface(Room)
    resource_name = 'room'

    class_permission_name = 'Room'

    list_columns = [
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
        room = RoomDAO.get_by_id(room_id)
        video_boxes = VideoBoxDAO.get_by_room(room.id)
        streams = []
        for box in video_boxes:
            video_streams = VideoStreamDAO.get_by_video_box(box.id)
            for video_stream in video_streams:
                streams.append({
                    'type': video_stream.stream_type,
                    'push_url': video_stream.push_url,
                    'broadcast_url': video_stream.broadcast_url,
                })
        return self.response(200, result={
            'name': room.name,
            'jabber_id': room.jabber_id,
            'streams': streams,
        })
