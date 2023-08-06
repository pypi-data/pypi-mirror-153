from typing import Generic, Iterable, TypeVar

from .model import AbstractModel

_Model = TypeVar('_Model', bound=AbstractModel)


class AbstractCompositeModel(AbstractModel, Generic[_Model]):
    def __init__(self, models: Iterable[_Model]):
        self._models = tuple(models)

    def __enter__(self):
        for m in self._models:
            m.__enter__()
        return self

    def __exit__(self, *exc):
        for m in self._models[::-1]:
            m.__exit__(*exc)
