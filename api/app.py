# -*- coding: utf-8 -*-
from werkzeug.wrappers import Response
from flask import Flask, jsonify


app = Flask(__name__)


class JsonResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, (dict, list)):
            response = jsonify(response)

        return super(JsonResponse, cls).force_type(response, environ)


app.response_class = JsonResponse


api_list = {
    'rooms': 'List rooms by page',
}


@app.route('/rooms', methods=['POST'])
def list_rooms():
    return {'code': 0}


def run_flask(listen_addr):
    import gunicorn.app.base

    class StandaloneApplication(gunicorn.app.base.BaseApplication):
        def __init__(self, app, options=None):
            self.application = app
            self.options = options or {}
            super(StandaloneApplication, self).__init__()

        def load_config(self):
            _config = dict([(key, val) for key, val in self.options.items()
                            if key in self.cfg.settings and val is not None])
            print(_config)
            for key, val in _config.items():
                self.cfg.set(key.lower(), val)

        def load(self):
            return self.application

    _options = {
        'bind': listen_addr,
        'workers': 4,
        'accesslog': '-',  # log to stdout
        'access_log_format': '%(h)s %(l)s %(t)s "%(r)s" %(s)s "%(a)s"'
    }
    StandaloneApplication(app, _options).run()
