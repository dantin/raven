# -*- coding: utf-8 -*-
import os

from flask_appbuilder import AppBuilder, SQLA
from flask_migrate import Migrate
from werkzeug.local import LocalProxy


APP_DIR = os.path.dirname(__file__)
appbuilder = AppBuilder(update_perms=False)
db = SQLA()
migrate = Migrate()
security_manager = LocalProxy(lambda: appbuilder.sm)
