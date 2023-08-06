from abc import ABCMeta, abstractmethod
from typing import Generic, Tuple, Type, TypeVar

from tp_interfaces.abstract.model import AbstractModel
from .update import AbstractUpdate, UpdateMode

_Update = TypeVar('_Update', bound=AbstractUpdate)


class AbstractUpdatableModel(AbstractModel, Generic[_Update]):

    def update(self, update: _Update) -> None:
        if update.mode is UpdateMode.add:
            self._add(update)
        else:
            self._remove(update)

    @abstractmethod
    def info(self) -> Tuple[_Update, ...]:
        pass

    @abstractmethod
    def _add(self, update: _Update) -> None:
        pass

    @abstractmethod
    def _remove(self, update: _Update) -> None:
        pass

    @property
    @abstractmethod
    def update_type(self) -> Type[_Update]:
        pass


class UpdatableModelMixin(AbstractUpdatableModel[_Update], Generic[_Update], metaclass=ABCMeta):
    def __init__(self, model: AbstractUpdatableModel):
        self._model = model

    def info(self) -> Tuple[_Update, ...]:
        return self._model.info()

    def update(self, update: _Update) -> None:
        self._model.update(update)

    def _add(self, update: _Update) -> None:
        self._model._add(update)

    def _remove(self, update: _Update) -> None:
        self._model._remove(update)

    @property
    def update_type(self) -> Type[_Update]:
        return self._model.update_type
