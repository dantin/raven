# -*- coding: utf-8 -*-
import logging
from typing import List

from raven.dao.base import BaseDAO
from raven.models import Room, VideoBox, VideoStream
from raven.extensions import db


logger = logging.getLogger(__name__)


class RoomDAO(BaseDAO):
    model_cls = Room
    base_filter = None

    @staticmethod
    def get_by_id(room_id: int) -> Room:
        room = RoomDAO.find_by_id(room_id)
        return room


class VideoBoxDAO(BaseDAO):
    model_cls = VideoBox
    base_filter = None

    @staticmethod
    def get_by_room(room_id: int) -> List[VideoBox]:
        session = db.session()
        video_boxes = session.query(
            VideoBox
        ).filter(
            VideoBox.room_id == room_id
        ).all()
        return video_boxes


class VideoStreamDAO(BaseDAO):
    model_cls = VideoStream
    base_filter = None

    def get_by_video_box(box_id: int) -> List[VideoStream]:
        session = db.session()
        video_streams = session.query(
            VideoStream
        ).filter(
            VideoStream.video_box_id == box_id
        ).all()
        return video_streams
