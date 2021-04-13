# -*- coding: utf-8 -*-

from flask_appbuilder.security.sqla.models import User
from sqlalchemy import Column, String


class RavenUser(User):
    __tablename__ = 'ab_user'
    jabber_id = Column(String(255))
