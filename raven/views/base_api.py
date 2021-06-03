# -*- coding: utf-8 -*-
import logging
from typing import List

from flask_appbuilder import ModelRestApi


logger = logging.getLogger(__name__)


class BaseRavenModelRestApi(ModelRestApi):
    """
    Extends FAB's ModelResApi to implement specific raven generic functionality.
    """
    csrf_exempt = False

    add_columns: List[str]
    edit_columns: List[str]
    list_columns: List[str]
    show_columns: List[str]

    def __init__(self) -> None:
        super().__init__()
