import typing
from abc import ABC, abstractmethod


class Selectable(ABC):
    def __init__(self, name: typing.AnyStr):
        self.name = name

    @abstractmethod
    def run(self):
        pass
