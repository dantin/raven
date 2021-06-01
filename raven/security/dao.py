# -*- coding: utf-8 -*-
import logging
from typing import List

from raven.dao.base import BaseDAO
from raven.security.models import RavenUser
from raven.extensions import db


logger = logging.getLogger(__name__)


class RavenUserDAO(BaseDAO):
    model_cls = RavenUser
    base_filter = None

    @staticmethod
    def get_roles_by_jabber_id(jabber_id: str) -> List[str]:
        session = db.session()
        user = session.query(
            RavenUser
        ).filter(
            RavenUser.jabber_id == jabber_id
        ).one_or_none()

        if not user:
            return []

        return [r.name for r in user.roles]
