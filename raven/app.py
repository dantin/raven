# -*- coding: utf-8 -*-
import logging
import os

from flask import Flask, g, render_template, redirect
from flask_appbuilder import expose, IndexView
from flask_babel import lazy_gettext

from raven.security import RavenSecurityManager
from raven.extensions import (
    APP_DIR,
    appbuilder,
    db,
    migrate,
)
from raven.utils.core import pessimistic_connection_handling


logger = logging.getLogger(__name__)


class RavenIndexView(IndexView):
    @expose("/")
    def index(self):
        user = g.user

        if user.is_anonymous:
            return redirect("/login/")
        return super().index()


def create_app() -> Flask:
    app = Flask(__name__)

    try:
        # Allow user to override config completely.
        config_module = os.environ.get('RAVEN_CONFIG', 'raven.config')
        app.config.from_object(config_module)

        app_initializer = app.config.get('APP_INITIALIZER', RavenAppInitializer)(app)
        app_initializer.init_app()

        return app
    except Exception as ex:
        logger.exception('Failed to create app')
        raise ex


class RavenAppInitializer:
    def __init__(self, app: Flask) -> None:
        super().__init__()

        self.flask_app = app
        self.config = app.config

    def init_app(self) -> None:
        """
        Main entry point which will delegate to other methods in
        order to fully init the app.
        """
        self.setup_db()
        self.configure_logging()
        with self.flask_app.app_context():
            self.init_app_in_ctx()

    def configure_logging(self) -> None:
        self.config['LOGGING_CONFIGURATOR'].configure_logging(
            self.config, self.flask_app.debug)

    def setup_db(self) -> None:
        db.init_app(self.flask_app)

        with self.flask_app.app_context():
            pessimistic_connection_handling(db.engine)

        migrate.init_app(self.flask_app, db=db, directory=APP_DIR + '/migrations')

    def init_app_in_ctx(self) -> None:
        self.configure_fab()
        self.init_views()

    def configure_fab(self) -> None:
        if self.config['SILENCE_FAB']:
            logging.getLogger('flask_appbuilder').setLevel(logging.ERROR)
        appbuilder.indexview = RavenIndexView
        appbuilder.security_manager_class = RavenSecurityManager
        appbuilder.init_app(self.flask_app, db.session)

    def init_views(self) -> None:
        db.create_all()
        from raven.views import (
            RoomModelView,
            VideoBoxModelView,
            VideoStreamModelView,
        )

        appbuilder.add_view(
            RoomModelView,
            'List Room',
            icon='fa-tachometer',
            label=lazy_gettext('Room List'),
            category='Video',
            category_icon='fa-server',
            category_label=lazy_gettext('Video Management'),
        )
        appbuilder.add_view(
            VideoBoxModelView,
            'List VideoBox',
            icon='fa-tachometer',
            label=lazy_gettext('VideoBox List'),
            category='Video',
        )
        appbuilder.add_view_no_menu(VideoStreamModelView, 'VideoStreamModelView')
        """
        Application wide 404 error handler
        """
        @appbuilder.app.errorhandler(404)
        def page_not_found(e):
            return (
                render_template(
                    "404.html",
                    base_template=appbuilder.base_template,
                    appbuilder=appbuilder
                ),
                404,
            )
