# -*- coding: utf-8 -*-
"""Package's main module!"""

from flask import Flask, current_app
from werkzeug.local import LocalProxy

from raven.extensions import appbuilder  # noqa # pylint: disable=unused-import
from raven.extensions import security_manager  # noqa # pylint: disable=unused-import


#  All of the fields located here should be considered legacy. The correct way
#  to declare "global" dependencies is to define it in extensions.py,
#  then initialize it in app.create_app().
app: Flask = current_app
conf = LocalProxy(lambda: current_app.config)
