# -*- coding: utf-8 -*-

from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_babel import lazy_gettext

from .models import Device, Room, Stream


class RoomModelView(ModelView):
    datamodel = SQLAInterface(Room)
    list_title = lazy_gettext('Room List')
    show_title = lazy_gettext('Room Detail')
    add_title = lazy_gettext('Add Room')
    edit_title = lazy_gettext('Edit Room')

    list_columns = [
        'name',
        'jabber_id',
    ]

    base_order = ('id', 'asc')


class StreamModelView(ModelView):
    datamodel = SQLAInterface(Stream)
    # base_permission = ['can_add', 'can_show']
    list_title = lazy_gettext('Stream List')
    show_title = lazy_gettext('Stream Detail')
    add_title = lazy_gettext('Add Stream')
    edit_title = lazy_gettext('Edit Stream')

    list_columns = ['push_url', 'broadcast_url']


class DeviceModelView(ModelView):
    datamodel = SQLAInterface(Device)
    related_views = [StreamModelView]
    show_template = 'appbuilder/general/model/show_cascade.html'

    list_title = lazy_gettext('Device List')
    show_title = lazy_gettext('Device Detail')
    add_title = lazy_gettext('Add Device')
    edit_title = lazy_gettext('Edit Device')

    list_columns = [
        'serial_no',
        'name',
        'room.name',
    ]

    label_columns = {
        'serial_no': lazy_gettext('Device No.'),
        'name': lazy_gettext('Device Name'),
        'room': lazy_gettext('Room'),
    }

    base_order = ('id', 'asc')

    show_fieldsets = [
        (
            lazy_gettext('Summary'),
            {'fields': ['serial_no', 'name']}
        ),
        (
            lazy_gettext('Room Detail'),
            {
                'fields': [
                    'room.name',
                    'room.jabber_id',
                ],
                'expanded': True,
            },
        ),
    ]
