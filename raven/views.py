# -*- coding: utf-8 -*-

from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_babel import lazy_gettext

from .models import VideoBox, Room, VideoStream


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


class VideoStreamModelView(ModelView):
    datamodel = SQLAInterface(VideoStream)
    # base_permission = ['can_add', 'can_show']
    list_title = lazy_gettext('VideoStream List')
    show_title = lazy_gettext('VideoStream Detail')
    add_title = lazy_gettext('Add VideoStream')
    edit_title = lazy_gettext('Edit VideoStream')

    list_columns = ['stream_type', 'push_url', 'broadcast_url']


class VideoBoxModelView(ModelView):
    datamodel = SQLAInterface(VideoBox)
    related_views = [VideoStreamModelView]
    show_template = 'appbuilder/general/model/show_cascade.html'

    list_title = lazy_gettext('VideoBox List')
    show_title = lazy_gettext('VideoBox Detail')
    add_title = lazy_gettext('Add VideoBox')
    edit_title = lazy_gettext('Edit VideoBox')

    list_columns = [
        'serial_no',
        'video_box_type',
        'name',
    ]

    label_columns = {
        'serial_no': lazy_gettext('VideoBox No.'),
        'name': lazy_gettext('VideoBox Name'),
        'room': lazy_gettext('Room'),
    }

    base_order = ('id', 'asc')

    show_fieldsets = [
        (
            lazy_gettext('Summary'),
            {'fields': ['serial_no', 'name', 'video_box_type']}
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
