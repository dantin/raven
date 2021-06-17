# -*- coding: utf-8 -*-
from typing import List, Optional, Type

from flask_appbuilder.models.filters import BaseFilter
from flask_appbuilder.models.sqla import Model
from flask_appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy.orm import Session

from raven.extensions import db


class BaseDAO:
    """
    BaseDAO, implement base CRUD sqlalchemy operations
    """

    """
    Child classes need to state the Model class so they don't need to implement basic
    create, update and delete methods
    """
    model_cls: Optional[Type[Model]] = None
    """
    Child classes can register base filtering to be aplied to all filter methods
    """
    base_filter: Optional[BaseFilter] = None

    @classmethod
    def find_by_id(cls, model_id: int, session: Session = None) -> Model:
        """Find a model by id."""
        session = session or db.session
        query = session.query(cls.model_cls)
        if cls.base_filter:
            data_model = SQLAInterface(cls.model_cls, session)
            query = cls.base_filter(
                'id', data_model
            ).apply(query, None)
        return query.filter_by(id=model_id).one_or_none()

    @classmethod
    def find_by_ids(cls, model_ids: List[int]) -> List[Model]:
        """Find a list of models by a list of ids."""
        id_col = getattr(cls.model_cls, 'id', None)
        if id_col is None:
            return []
        query = db.session.query(cls.model_cls).filter(id_col.in_(model_ids))
        if cls.base_filter:
            data_model = SQLAInterface(cls.model_cls, db.session)
            query = cls.base_filter(
                'id', data_model
            ).apply(query, None)
        return query.all()

    @classmethod
    def find_all(cls) -> List[Model]:
        """Get all that fit the `base_filter`."""
        query = db.session.query(cls.model_cls)
        if cls.base_filter:
            data_model = SQLAInterface(cls.model_cls, db.session)
            query = cls.base_filter(  # pylint: disable=not-callable
                'id', data_model
            ).apply(query, None)
        return query.all()
