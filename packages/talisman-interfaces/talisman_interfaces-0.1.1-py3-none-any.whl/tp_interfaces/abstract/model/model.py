import pickle
from abc import ABCMeta
from contextlib import AbstractContextManager
from pathlib import Path
from typing import Type, TypeVar


_Model = TypeVar('_Model', bound='AbstractModel')


class AbstractModel(AbstractContextManager, metaclass=ABCMeta):
    def __enter__(self: _Model) -> _Model:
        return self

    def __getstate__(self):
        return self.__dict__.copy()

    @classmethod
    def load(cls: Type[_Model], path: Path) -> _Model:
        if path.suffix == '.dvc':
            import dvc.api
            # problem with dvc.api.open: https://github.com/iterative/dvc/issues/4667
            model = pickle.loads(dvc.api.read(path.with_suffix(''), mode='rb'))
        else:
            with path.open('rb') as f:
                model = pickle.load(f)
        if not isinstance(model, cls):
            raise Exception(f"Model at {path} is not an instance of {cls}")
        return model

    def save(self, path: Path) -> None:
        if path.exists():
            raise Exception(f"Model saving path exists: {path}")

        with path.open('wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
