from collections import defaultdict
from typing import Callable, Dict, Generic, List, Optional, Sequence, Tuple, Type, TypeVar

from tdm.abstract.datamodel import AbstractTreeDocumentContent
from tdm.datamodel import TalismanDocument

from tp_interfaces.abstract.model import AbstractCompositeModel
from tp_interfaces.abstract.schema import ImmutableBaseModel
from .processor import AbstractDocumentProcessor

_DocumentContent = TypeVar('_DocumentContent', bound=AbstractTreeDocumentContent)
_Config = TypeVar('_Config', bound=ImmutableBaseModel)
_Category = TypeVar('_Category')


class AbstractCategoryAwareDocumentProcessor(
    AbstractCompositeModel[AbstractDocumentProcessor[_Config, _DocumentContent]],
    AbstractDocumentProcessor[_Config, _DocumentContent], Generic[_Config, _DocumentContent, _Category]
):
    def __init__(self,
                 category2processor: Dict[_Category, AbstractDocumentProcessor[_Config, _DocumentContent]],
                 categorizer: Callable[[TalismanDocument[_DocumentContent]], _Category]
                 ):
        self._category2processor = dict(category2processor)
        super().__init__(self._category2processor.values())
        self._models: Tuple[AbstractDocumentProcessor[_Config, _DocumentContent], ...]
        self._categorizer = categorizer

    def process_doc(self, document: TalismanDocument[_DocumentContent], config: _Config) -> TalismanDocument[_DocumentContent]:
        return self.process_docs([document], config)[0]

    def process_docs(self, documents: Sequence[TalismanDocument[_DocumentContent]], config: _Config) \
            -> Tuple[TalismanDocument[_DocumentContent], ...]:
        category2doc = defaultdict(dict)
        processed_docs: List[Optional[TalismanDocument[_DocumentContent]]] = [None] * len(documents)

        for i, doc in enumerate(documents):
            category = self._categorizer(doc)
            category2doc[category].update({i: doc})

        for category, docs in category2doc.items():
            processor = self._category2processor[category]
            docs_ = processor.process_docs(tuple(docs.values()), config)
            for id_, doc in zip(docs, docs_):
                processed_docs[id_] = doc

        return tuple(processed_docs)

    @property
    def config_type(self) -> Type[_Config]:
        return self._models[0].config_type
