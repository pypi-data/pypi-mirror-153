from abc import abstractmethod
from typing import Generic, Type, TypeVar

from .model import AbstractModel

_Model = TypeVar('_Model', bound=AbstractModel)
_Wrapper = TypeVar('_Wrapper', bound='AbstractModelWrapper')


class AbstractModelWrapper(AbstractModel, Generic[_Model]):
    def __init__(self, model: _Model):
        self._model = model

    def __enter__(self):
        self._model.__enter__()
        return self

    def __exit__(self, *exc):
        self._model.__exit__(*exc)

    @classmethod
    def from_config(cls: Type[_Wrapper], model: _Model, config: dict) -> _Wrapper:
        kwargs = cls.parse_config(config)
        return cls(model, **kwargs)

    @staticmethod
    @abstractmethod
    def parse_config(config: dict) -> dict:
        pass
