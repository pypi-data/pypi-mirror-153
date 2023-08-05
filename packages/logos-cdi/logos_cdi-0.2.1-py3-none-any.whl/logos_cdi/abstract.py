from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TypeVar, Type

R = TypeVar('R')


class AbstractContainer(ABC):
    """Abstract Container Class"""

    @abstractmethod
    def get(self, name: str, context: AbstractContainer = None, _type: Type[R] = object) -> R:
        raise NotImplementedError('Please implement this method')

    @abstractmethod
    def has(self, name: str, context: AbstractContainer = None) -> bool:
        raise NotImplementedError('Please implement this method')

    def resource_names(self) -> list:
        raise NotImplementedError('Please implement this method')


class AbstractResource(ABC):
    """Abstract Resource Class"""

    @abstractmethod
    def resolve(self, container: AbstractContainer, _name: str = None):
        raise NotImplementedError('Please implement this method')


class AbstractContextManager(ABC):

    def __init__(self, context: AbstractContainer):
        self.context = context

    @abstractmethod
    async def __aenter__(self) -> AbstractContainer:
        raise NotImplementedError('Please implement this method')

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError('Please implement this method')