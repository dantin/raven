# -*- coding: utf-8 -*-
import logging

from flask_appbuilder.security.sqla.manager import SecurityManager


logger = logging.getLogger(__name__)


class RavenSecurityManager(SecurityManager):

    userstatschartview = None

    def create_custom_permissions(self) -> None:
        """
        Create custom FAB permissions.
        """
        self.add_permission_view_menu("all_datasource_access", "all_datasource_access")
        self.add_permission_view_menu("all_database_access", "all_database_access")
        self.add_permission_view_menu("all_query_access", "all_query_access")

    def sync_role_definitions(self) -> None:
        """ Initialize the Raven application with security roles and such."""
        # from raven import conf

        logger.info("Syncing role definition")

        self.create_custom_permissions()

        # commit role and view menu updates
        self.get_session.commit()
