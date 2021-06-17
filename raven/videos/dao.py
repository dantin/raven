# -*- coding: utf-8 -*-
import logging

from flask_appbuilder.security.sqla.models import Role

from raven.dao.base import BaseDAO
from raven.extensions import db
from raven.models import Room
from raven.security.models import RavenUser
from raven.security.dao import RavenUserDAO


logger = logging.getLogger(__name__)


class RoomDAO(BaseDAO):
    model_cls = Room
    base_filter = None

    @staticmethod
    def get_by_jabber_id(jabber_id: str) -> Room:
        rooms = RoomDAO.find_all()
        if not rooms:
            return []

        logger.debug(f'found {len(rooms)} rooms')

        roles = RavenUserDAO.get_roles_by_jabber_id(jabber_id)

        session = db.session()
        users = session.query(
            RavenUser
        ).filter(
            RavenUser.roles.any(Role.name.in_(roles))
        ).all()

        if not users:
            return []

        logger.debug(f'found {len(users)} users')

        i = 0
        for u in users:
            if jabber_id == u.jabber_id:
                break
            i += 1

        logger.debug(f'user pos {i}')
        i = i % len(rooms)
        logger.debug(f'room index {i}')

        return rooms[i]
