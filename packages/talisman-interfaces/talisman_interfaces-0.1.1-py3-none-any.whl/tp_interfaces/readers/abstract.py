from abc import ABCMeta, abstractmethod
from typing import Callable, Dict, Generic, Iterator, Optional, Type, TypeVar, Union

from tdm.abstract.datamodel import AbstractFact, AbstractTreeDocumentContent, FactStatus
from tdm.datamodel import TalismanDocument, TalismanSpan
from tdm.datamodel.fact import ConceptFact, ValueFact

EntityFactType = Union[Type[ConceptFact], Type[ValueFact]]
Label2FactType = Dict[str, EntityFactType]

_Content = TypeVar('_Content', bound=AbstractTreeDocumentContent)


class AbstractReader(Generic[_Content], metaclass=ABCMeta):
    @abstractmethod
    def read(self) -> Iterator[TalismanDocument[_Content]]:
        pass


def label_span2fact(default_type: EntityFactType,
                    label2facttype: Optional[Label2FactType] = None,
                    status: FactStatus = FactStatus.APPROVED) \
        -> Callable[[str, TalismanSpan], AbstractFact]:
    mapping = dict(label2facttype) if label2facttype is not None else {}

    def create_fact(label: str, span: TalismanSpan) -> AbstractFact:
        return mapping.get(label, default_type)(None, status, label, None, [span])

    return create_fact
