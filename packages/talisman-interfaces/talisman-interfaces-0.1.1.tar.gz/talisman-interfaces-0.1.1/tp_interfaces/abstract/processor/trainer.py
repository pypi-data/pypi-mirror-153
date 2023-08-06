from abc import ABCMeta, abstractmethod
from typing import Generic, Iterable, TypeVar

from tdm.abstract.datamodel import AbstractTreeDocumentContent
from tdm.datamodel import TalismanDocument

from .processor import AbstractDocumentProcessor

_DocumentContent = TypeVar('_DocumentContent', bound=AbstractTreeDocumentContent)
_Processor = TypeVar('_Processor', bound=AbstractDocumentProcessor)


class AbstractTrainer(Generic[_Processor, _DocumentContent], metaclass=ABCMeta):

    @abstractmethod
    def train(self,
              train_docs: Iterable[TalismanDocument[_DocumentContent]],
              dev_docs: Iterable[TalismanDocument[_DocumentContent]] = None) \
            -> _Processor:
        pass
