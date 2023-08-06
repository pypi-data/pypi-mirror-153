from abc import ABCMeta, abstractmethod
from contextlib import AbstractContextManager
from typing import Any, Callable, Dict, FrozenSet, Generator, Generic, Iterable, Iterator, NamedTuple, Optional, Tuple, Type, TypeVar

from tdm.abstract.datamodel import AbstractFact, AbstractTalismanDocument
from tdm.datamodel import ConceptFact

from tp_interfaces.abstract import ImmutableBaseModel


class DBProperty(NamedTuple):
    name: str
    value: Any


class DBRelation(NamedTuple):
    source_id: str
    target_id: str
    type: str
    properties: Tuple[DBProperty, ...] = tuple()


class DBConcept:
    __slots__ = ('_id', '_name', '_type', '_aliases', '_in_relations', '_out_relations', '_properties')

    def __init__(
            self,
            id_: str,
            name: str,
            type_: Optional[str],
            aliases: Iterable[str],
            in_relations: Iterable[DBRelation],
            out_relations: Iterable[DBRelation],
            properties: Iterable[DBProperty] = None
    ):
        self._id = id_
        self._name = name
        self._type = type_
        self._aliases = frozenset(aliases)

        self._in_relations = self._get_unique_relations(in_relations)
        self._out_relations = self._get_unique_relations(out_relations)

        for rel in self._in_relations:
            if rel.target_id != id_:
                raise Exception(f"DBConcept {id_} is not target in provided in relation {rel}")

        for rel in self._out_relations:
            if rel.source_id != id_:
                raise Exception(f"DBConcept {id_} is not source in provided in relation {rel}")

        self._properties = self._get_unique_properties(properties) if properties else tuple()

    @property
    def id_(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> str:
        return self._type

    @property
    def aliases(self) -> FrozenSet[str]:
        return self._aliases

    @property
    def in_relations(self) -> Tuple[DBRelation, ...]:
        return self._in_relations

    @property
    def out_relations(self) -> Tuple[DBRelation, ...]:
        return self._out_relations

    @property
    def relations(self) -> Tuple[DBRelation, ...]:
        return self._in_relations + self._out_relations

    @property
    def properties(self) -> Tuple[DBProperty, ...]:
        return self._properties

    def __repr__(self):
        return repr((self.id_, self._name))

    def __eq__(self, other):
        if not isinstance(other, DBConcept):
            return NotImplemented

        def tupled(obj: DBConcept):
            return obj._id, obj._name, obj._type, obj._aliases, obj._in_relations, obj._out_relations, obj._properties

        return tupled(self) == tupled(other)

    def __hash__(self):
        return hash(self._id)

    @staticmethod
    def _get_unique(params: Iterable) -> Generator:
        #  FIXME: think about better solution
        unique_properties = []
        for param in params:
            if param not in unique_properties:
                unique_properties.append(param)
                yield param

    def _get_unique_properties(self, properties: Iterable[DBProperty]) -> Tuple[DBProperty, ...]:
        return tuple(self._get_unique(properties))

    def _get_unique_relations(self, relations: Iterable[DBRelation]) -> Tuple[DBRelation, ...]:
        return tuple(map(lambda r: DBRelation(r.source_id, r.target_id, r.type, self._get_unique_properties(r.properties)),
                         self._get_unique(relations)))

    @classmethod
    def create(cls, id_: Optional[str], name: str, type_: Optional[str], aliases: Iterable[str], in_relations: Iterable[DBRelation],
               out_relations: Iterable[DBRelation], properties: Iterable[DBProperty] = None):
        return cls(id_, name, type_, aliases, in_relations, out_relations, properties)


class DBRemoteConcept(DBConcept):
    def __init__(self, id_: Optional[str], name: str, type_: Optional[str], aliases: Iterable[str], in_relations: Iterable[DBRelation],
                 out_relations: Iterable[DBRelation], properties: Iterable[DBProperty] = None):
        super().__init__(id_ or "DBRemoteConcept id: " + str(id(self)), name, type_, aliases, in_relations, out_relations, properties)

    @classmethod
    def create(cls, id_: Optional[str], name: str, type_: Optional[str], aliases: Iterable[str], in_relations: Iterable[DBRelation],
               out_relations: Iterable[DBRelation], properties: Iterable[DBProperty] = None):
        return cls(id_, name, type_, aliases, in_relations, out_relations, properties)


class MentionConceptFeatures(NamedTuple):
    commonness: float
    dot_similarity: Optional[float] = None
    cos_similarity: Optional[float] = None


class MentionCandidates(object):
    __slots__ = ('_candidates_set', '_candidates')

    def __init__(self, candidates: Dict[DBConcept, MentionConceptFeatures]):
        if not candidates:
            raise Exception("Provided empty candidates")

        self._candidates_set = frozenset(candidates)
        self._candidates = dict(candidates)

    @property
    def candidates(self) -> FrozenSet[DBConcept]:
        return self._candidates_set

    def features_for(self, concept: DBConcept) -> MentionConceptFeatures:
        return self._candidates[concept]

    def __eq__(self, other):
        if not isinstance(other, MentionCandidates):
            return NotImplemented
        return self._candidates == other._candidates

    def __repr__(self):
        return repr(self._candidates)


class DMBRuleConfigInterface(ImmutableBaseModel):
    pass


_DMBRuleConfigInterface = TypeVar('_DMBRuleConfigInterface', bound=DMBRuleConfigInterface)


class DisambiguationKB(AbstractContextManager, Generic[_DMBRuleConfigInterface], metaclass=ABCMeta):
    @abstractmethod
    def get_candidates(self, doc: AbstractTalismanDocument) -> Dict[ConceptFact, MentionCandidates]:
        pass

    @abstractmethod
    def get_rule_config(self) -> Type[_DMBRuleConfigInterface]:
        pass

    @abstractmethod
    def get_candidates_by_rules(
            self, doc: AbstractTalismanDocument, filter_: Callable[[AbstractFact], bool], config: _DMBRuleConfigInterface
    ) -> Iterator[Tuple[ConceptFact, Tuple[str, ...]]]:
        pass

    def load_new_concepts_and_mentions(self, concepts: Iterable[DBConcept], docs: Iterable[AbstractTalismanDocument]):
        self.load_new_concepts(concepts)
        self.load_new_mentions(docs)

    @abstractmethod
    def load_new_concepts(self, concepts: Iterable[DBConcept]) -> None:
        pass

    @abstractmethod
    def load_new_mentions(self, docs: Iterable[AbstractTalismanDocument]) -> None:
        pass

    @abstractmethod
    def get_concepts_num(self) -> int:
        pass

    @abstractmethod
    def bind_facts_and_load_docs(self, docs: Tuple[AbstractTalismanDocument, ...]):
        pass

    @classmethod
    @abstractmethod
    def from_config(cls, config: dict) -> 'DisambiguationKB':
        pass


class AbstractConceptReader(metaclass=ABCMeta):
    @abstractmethod
    def read(self) -> Iterator[DBConcept]:
        pass
