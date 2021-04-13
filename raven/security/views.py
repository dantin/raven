# -*- coding: utf-8 -*-

from flask_appbuilder.security.views import UserDBModelView
from flask_babel import lazy_gettext


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
