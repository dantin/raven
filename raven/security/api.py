# -*- coding: utf-8 -*-
import logging

from flask import Response
from flask_appbuilder import expose
from flask_appbuilder.api import BaseApi, safe
from flask_appbuilder.security.decorators import protect

from raven.security.dao import RavenUserDAO


logger = logging.getLogger(__name__)


class SecurityRestApi(BaseApi):
    resource_name = 'security'
    allow_browser_login = True

    @expose('/<jabber_id>/roles', methods=['GET'])
    @protect()
    @safe
    def get_roles(self, jabber_id: str) -> Response:
        logger.info(f'get roles of {jabber_id}')

        roles = RavenUserDAO.get_roles_by_jabber_id(jabber_id)
        return self.response(200, result={
            'jabber_id': jabber_id,
            'roles': roles,
        })
