from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import Generic, Iterable, TextIO, TypeVar

from tdm.abstract.datamodel import AbstractTreeDocumentContent
from tdm.datamodel import TalismanDocument

_Content = TypeVar('_Content', bound=AbstractTreeDocumentContent)


class AbstractSerializer(Generic[_Content], metaclass=ABCMeta):
    @abstractmethod
    def serialize(self, doc: TalismanDocument[_Content], stream: TextIO):
        pass

    @staticmethod
    def _check_stream(stream: TextIO):
        if stream.closed or not stream.writable():
            raise Exception("stream  is closed or not writeable")


class AbstractPathSerializer(Generic[_Content], metaclass=ABCMeta):
    @abstractmethod
    def serialize(self, docs: Iterable[TalismanDocument[_Content]], path: Path):
        pass
