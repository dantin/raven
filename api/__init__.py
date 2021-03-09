# -*- coding: utf-8 -*-

from api.app import run_flask


def run_api_server(bind_addr):
    run_flask(bind_addr)
