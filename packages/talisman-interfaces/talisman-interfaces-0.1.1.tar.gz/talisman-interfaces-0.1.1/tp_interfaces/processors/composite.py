from typing import Iterable, Optional, Sequence, Tuple, Type, TypeVar

from tdm.abstract.datamodel import AbstractTreeDocumentContent
from tdm.datamodel import TalismanDocument

from tp_interfaces.abstract import AbstractCompositeModel, AbstractDocumentProcessor, ImmutableBaseModel

_DocumentContent = TypeVar('_DocumentContent', bound=AbstractTreeDocumentContent)
_Config = TypeVar('_Config', bound=ImmutableBaseModel)


class SequentialConfig(ImmutableBaseModel):
    configs: Optional[Tuple[ImmutableBaseModel, ...]]


class SequentialDocumentProcessor(
    AbstractCompositeModel[AbstractDocumentProcessor],
    AbstractDocumentProcessor[SequentialConfig, _DocumentContent]
):

    def __init__(self, processors: Iterable[AbstractDocumentProcessor]):
        AbstractCompositeModel[AbstractDocumentProcessor].__init__(self, processors)
        AbstractDocumentProcessor.__init__(self)

        config_types = tuple(processor.config_type for processor in self._models)

        class _SequentialConfig(SequentialConfig):
            configs: Optional[Tuple[config_types]]

        self._config_type = _SequentialConfig
        self._config_types = config_types

    def process_doc(self, document: TalismanDocument[_DocumentContent], config: _Config) -> TalismanDocument[_DocumentContent]:
        return self.process_docs([document], config)[0]

    def process_docs(
            self,
            documents: Sequence[TalismanDocument[_DocumentContent]],
            config: SequentialConfig
    ) -> Tuple[TalismanDocument[_DocumentContent], ...]:
        configs = config.configs if config.configs is not None else [model.config_type() for model in self._models]
        for processor_idx, processor in enumerate(self._models):
            documents = processor.process_docs(documents, configs[processor_idx])
        return documents

    @property
    def config_type(self) -> Type[SequentialConfig]:
        return self._config_type
