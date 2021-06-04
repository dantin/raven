# -*- coding: utf-8 -*-
import os

from flask_appbuilder import AppBuilder, SQLA
from flask_migrate import Migrate
from werkzeug.local import LocalProxy

from raven.remote.client import EjabberdOpenAPI


APP_DIR = os.path.dirname(__file__)
appbuilder = AppBuilder(update_perms=False)
db = SQLA()
migrate = Migrate()
security_manager = LocalProxy(lambda: appbuilder.sm)
ejabber_api = EjabberdOpenAPI()
