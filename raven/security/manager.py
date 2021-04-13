# -*- coding: utf-8 -*-
import logging

from flask_appbuilder.security.sqla.manager import SecurityManager

from .models import RavenUser
from .views import RavenUserDBModelView


logger = logging.getLogger(__name__)


class RavenSecurityManager(SecurityManager):

    userstatschartview = None
    user_model = RavenUser
    userdbmodelview = RavenUserDBModelView

    def create_custom_permissions(self) -> None:
        """
        Create custom FAB permissions.
        """
        pass

    def sync_role_definitions(self) -> None:
        """ Initialize the Raven application with security roles and such."""
        # from raven import conf

        logger.info("Syncing role definition")

        self.create_custom_permissions()

        # commit role and view menu updates
        self.get_session.commit()
