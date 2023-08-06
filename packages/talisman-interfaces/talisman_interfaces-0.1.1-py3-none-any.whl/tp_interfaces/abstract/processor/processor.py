from abc import ABCMeta, abstractmethod
from functools import partial
from itertools import chain
from typing import Generic, Iterator, Sequence, Tuple, Type, TypeVar

from more_itertools import ichunked
from tdm.abstract.datamodel import AbstractTreeDocumentContent
from tdm.datamodel import TalismanDocument

from tp_interfaces.abstract.model import AbstractModel
from tp_interfaces.abstract.schema import ImmutableBaseModel

_DocumentContent = TypeVar('_DocumentContent', bound=AbstractTreeDocumentContent)
_Config = TypeVar('_Config', bound=ImmutableBaseModel)


class AbstractDocumentProcessor(AbstractModel, Generic[_Config, _DocumentContent], metaclass=ABCMeta):

    @abstractmethod
    def process_doc(self, document: TalismanDocument[_DocumentContent], config: _Config) -> TalismanDocument[_DocumentContent]:
        pass

    def process_docs(self, documents: Sequence[TalismanDocument[_DocumentContent]], config: _Config) \
            -> Tuple[TalismanDocument[_DocumentContent], ...]:
        return tuple(map(partial(self.process_doc, config=config), documents))

    def process_stream(self, documents: Iterator[TalismanDocument[_DocumentContent]], config: _Config, batch_size: int) \
            -> Iterator[TalismanDocument[_DocumentContent]]:
        return chain.from_iterable(map(partial(self.process_docs, config=config), map(tuple, ichunked(documents, batch_size))))

    @property
    @abstractmethod
    def config_type(self) -> Type[_Config]:
        pass
