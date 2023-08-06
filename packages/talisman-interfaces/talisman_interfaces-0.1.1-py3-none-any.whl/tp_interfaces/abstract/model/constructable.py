from abc import abstractmethod
from typing import Sequence, Type, TypeVar

from .model import AbstractModel

_Model = TypeVar('_Model', bound='AbstractConfigConstructableModel')


class AbstractConfigConstructableModel(AbstractModel):
    @classmethod
    @abstractmethod
    def from_config(cls: Type[_Model], config: dict) -> _Model:
        pass


class AbstractMultipleConfigConstructableModel(AbstractConfigConstructableModel):
    @classmethod
    def from_config(cls: Type[_Model], config: dict) -> _Model:
        return cls.from_configs([config])

    @classmethod
    @abstractmethod
    def from_configs(cls: Type[_Model], configs: Sequence[dict]) -> _Model:
        pass
