# -*- coding: utf-8 -*-
from typing import Optional


class RavenException(Exception):
    status = 500
    message = ''

    def __init__(
        self, message: str = "", exception: Optional[Exception] = None,
    ) -> None:
        if message:
            self.message = message
        self._exception = exception
        super().__init__(self.message)

    @property
    def exception(self) -> Optional[Exception]:
        return self._exception


class RemoteAPIError(RavenException):
    message = 'remote API error'
