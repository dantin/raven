# -*- coding: utf-8 -*-
from dataclass import dataclass
from enum import Enum
from typing import Any, Dict, Optional


class RavenErrorType(str, Enum):
    """
    Types of errors that can exist within Raven.
    """
    # DB Engine errors
    GENERIC_DB_ENGINE_ERROR = 'GENERIC_DB_ENGINE_ERROR'

    # Gneric errors
    GENERIC_BACKEND_ERROR = 'GENERIC_BACKEND_ERROR'


ERROR_TYPES_TO_ISSUE_CODES_MAPPING = {
    RavenErrorType.GENERIC_DB_ENGINE_ERROR: [
        {
            'code': 1002,
            "message": 'Issue 1002 - The database returned an unexpected error.',
        }
    ],
    RavenErrorType.GENERIC_BACKEND_ERROR: [
        {
            'code': 1011,
            'message': 'Issue 1011 - Superset encountered an unexpected error.',
        },
    ],
}


class ErrorLevel(str, Enum):
    """
    Levels of erros that can exists with Raven.
    """

    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'


@dataclass
class RavenError:
    """
    An error that is returned to a client.
    """

    message: str
    error_type: RavenErrorType
    level: ErrorLevel
    extra: Optional[Dict[str, Any]] = None

    def __post_init__(self) -> None:
        """
        Mutate the extra params with user facing error codes that map to backend
        errors.
        """
        issue_codes = ERROR_TYPES_TO_ISSUE_CODES_MAPPING.get(self.error_type)
        if issue_codes:
            self.extra = self.extra or {}
            self.extra.update({'issue_codes': issue_codes})
