# -*- coding: utf-8 -*-
import logging

from raven.dao.base import BaseDAO
from raven.extensions import db
from raven.models import Room


logger = logging.getLogger(__name__)


class RoomDAO(BaseDAO):
    model_cls = Room
    base_filter = None

    @staticmethod
    def get_by_id(room_id: int) -> Room:
        return RoomDAO.find_by_id(room_id)

    @staticmethod
    def get_by_jabber_id(jabber_id: str) -> Room:
        session = db.session()
        return session.query(
            Room
        ).filter(
            Room.jabber_id == jabber_id
        ).one_or_none()
