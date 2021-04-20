# -*- coding: utf-8 -*-
import logging

from flask_appbuilder.models.sqla.interface import SQLAInterface

from raven.views.base_api import BaseRavenModelRestApi
from raven.models import Room


logger = logging.getLogger(__name__)


class RoomRestApi(BaseRavenModelRestApi):
    datamodel = SQLAInterface(Room)
    resource_name = "room"

    class_permission_name = "Room"

    list_columns = [
        'name',
        'jabber_id',
    ]
