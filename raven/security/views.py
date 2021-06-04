# -*- coding: utf-8 -*-
import logging

from flask_appbuilder.security.views import UserDBModelView
from flask_babel import lazy_gettext

from raven.extensions import ejabber_api


logger = logging.getLogger(__name__)


class RavenUserDBModelView(UserDBModelView):
    show_fieldsets = [
        (
            lazy_gettext('User info'),
            {'fields': ['username', 'active', 'roles', 'login_count', 'jabber_id']},
        ),
        (
            lazy_gettext('Personal Info'),
            {'fields': ['first_name', 'last_name', 'email'], 'expanded': True},
        ),
        (
            lazy_gettext('Audit Info'),
            {
                'fields': [
                    'last_login',
                    'fail_login_count',
                    'created_on',
                    'created_by',
                    'changed_on',
                    'changed_by',
                ],
                'expanded': False,
            },
        ),
    ]

    user_show_fieldsets = [
        (
            lazy_gettext('User info'),
            {'fields': ['username', 'active', 'roles', 'login_count', 'jabber_id']},
        ),
        (
            lazy_gettext('Personal Info'),
            {'fields': ['first_name', 'last_name', 'email'], 'expanded': True},
        ),
    ]

    add_columns = [
        'first_name',
        'last_name',
        'username',
        'active',
        'email',
        'roles',
        'jabber_id',
        'password',
        'conf_password',
    ]

    list_columns = [
        'first_name',
        'last_name',
        'username',
        'email',
        'active',
        'roles',
    ]
    edit_columns = [
        'first_name',
        'last_name',
        'username',
        'active',
        'email',
        'roles',
        'jabber_id',
    ]

    def post_update(self, item):
        if not item.jabber_id:
            return

        self._sync_account(item.jabber_id)

    def post_add(self, item):
        if not item.jabber_id:
            return

        self._sync_account(item.jabber_id)

    def pre_delete(self, item):
        if not item.jabber_id:
            return

        jabber_id = item.jabber_id
        logger.debug(f'delete {jabber_id} from ejabber')
        ejabber_api.unregister(jabber_id)

    def _sync_account(self, jabber_id: str) -> None:
        logger.debug(f'sync ejabber with account {jabber_id}')

        if not ejabber_api.check_account(jabber_id):
            ejabber_api.register(jabber_id)
