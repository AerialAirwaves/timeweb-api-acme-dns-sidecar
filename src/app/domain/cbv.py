from abc import ABC
from functools import cached_property

from fastapi import APIRouter


class ClassBasedView(ABC):
    @cached_property
    def router(self) -> APIRouter:
        raise NotImplementedError
