import itertools
import json
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Iterator, List, Tuple

from tp_interfaces.knowledge_base.interfaces import AbstractConceptReader, DBConcept, DBProperty, DBRelation, DBRemoteConcept


class JSONConceptReader(AbstractConceptReader):
    def __init__(self, filepath: Path):
        self._path = filepath

    def read(self) -> Iterator[DBConcept]:
        raw_objects = list(self._read_raw_objs())
        local_ids = {raw_obj["id"] for raw_obj in raw_objects if "id" in raw_obj}

        in_relations = defaultdict(list)
        out_relations = defaultdict(list)
        counter = itertools.count()

        for raw_obj in raw_objects:
            is_local = "id" in raw_obj
            id_ = raw_obj["id"] if is_local else f"DBRemoteConcept id: {next(counter)}"
            out_rels = []

            for rel in self._parse_raw_rels(raw_obj, id_):
                current_rel = rel
                if rel.target_id in local_ids:
                    in_relations[rel.target_id].append(rel)
                else:
                    current_id = f"DBRemoteConcept id: {next(counter)}"
                    current_rel = DBRelation(id_, current_id, rel.type, rel.properties)
                    yield DBRemoteConcept(current_id, rel.target_id, None, [], [current_rel], [], [])

                out_rels.append(current_rel)

            if not is_local:
                yield DBRemoteConcept(id_, raw_obj["name"], raw_obj["type"], [], [], out_rels, [])
            else:
                out_relations[id_] = out_rels

        for raw_obj in raw_objects:
            if "id" not in raw_obj:
                continue
            obj_in_rels = in_relations[raw_obj["id"]]
            obj_out_rels = out_relations[raw_obj["id"]]
            obj_prop = self._parse_raw_properties(raw_obj.get('properties', None))
            yield DBConcept(raw_obj["id"], raw_obj["name"], raw_obj["type"], raw_obj["aliases"], obj_in_rels, obj_out_rels, obj_prop)

    def _read_raw_objs(self) -> Iterator[dict]:
        with self._path.open('r', encoding='utf-8') as f:
            yield from map(json.loads, f)

    def _parse_raw_rels(self, raw_obj: dict, id_: str) -> Iterator[DBRelation]:
        return (DBRelation(id_, raw_rel["target"], raw_rel["type"], tuple(self._parse_raw_properties(raw_rel.get('properties', None))))
                for raw_rel in raw_obj["relations"])

    @staticmethod
    def _parse_raw_properties(raw_properties: tuple) -> Iterator[DBProperty]:
        if not raw_properties:
            return tuple()
        return (DBProperty(property_['name'], property_['value']) for property_ in raw_properties)


class TypesMappingFilteringReader(AbstractConceptReader):
    def __init__(
            self,
            reader: AbstractConceptReader,
            concepts_types_mapping: Dict[str, str],
            relations_types_mapping: Dict[str, Dict[str, Any]],
            properties_types_mapping: Dict[str, Dict[str, str]]
    ):
        """
        :param reader: reader to wrap
        :param concepts_types_mapping: Mapping [old concept type -> new concept type].
            If old concept type is not in mapping it will be skipped.
        :param relations_types_mapping:
            Mapping [old_rel_type] -> [source_concept_old_type, target_concept_old_type, new_rel_type, need_to_flip].
            If relation signature not in mapping it will be skipped.
            If need_to_flip flag is set for relation its source and target concepts will be flipped in new relation.
        :param properties_types_mapping:
            Mapping [old concept type -> [old property -> new property]]
        """
        self._reader = reader
        self._concepts_types_mapping = deepcopy(concepts_types_mapping)
        self._relations_types_mapping = deepcopy(relations_types_mapping)
        self._properties_types_mapping = deepcopy(properties_types_mapping)

    def read(self) -> Iterator[DBConcept]:
        id2concept: Dict[str, DBConcept] = {}
        id2type: Dict[str, str] = {}
        id2in_relations: Dict[str, List[DBRelation]] = {}
        id2out_relations: Dict[str, List[DBRelation]] = {}

        for concept in self._reader.read():
            id2concept[concept.id_] = concept
            id2type[concept.id_] = concept.type

        for id_, concept in id2concept.items():
            id2in_relations[id_], id2out_relations[id_] = self._process_relations(concept, id2type)

        for id_, concept in id2concept.items():
            if id2type[id_] not in self._concepts_types_mapping:
                continue
            prop_map = self._properties_types_mapping[id2type[id_]]
            properties = tuple(DBProperty(prop_map.get(prop.name, prop.name), prop.value)
                               for prop in concept.properties) if concept.properties else tuple()
            params = {
                "id_": concept.id_,
                "name": concept.name,
                "type_": self._concepts_types_mapping.get(id2type[id_]),
                "aliases": concept.aliases,
                "in_relations": id2in_relations[id_],
                "out_relations": id2out_relations[id_],
                "properties": properties
            }

            yield concept.create(**params)

    def _process_relations(self, concept: DBConcept, id2types: Dict[str, str]) -> Tuple[List[DBRelation], List[DBRelation]]:
        in_relations, out_relations = [], []

        for rel in concept.relations:
            if rel.type not in self._relations_types_mapping:
                continue

            rel_map = self._relations_types_mapping[rel.type]
            source_id, target_id = (rel.target_id, rel.source_id) if rel_map["flip_relation"] else (rel.source_id, rel.target_id)

            source_type = rel_map["source_type"]
            if id2types[source_id] is None:
                id2types[source_id] = rel_map["source_type"]
            elif id2types[source_id] != source_type:
                continue

            target_type = rel_map["target_type"]
            if id2types[target_id] is None:
                id2types[target_id] = target_type
            elif target_type != id2types[target_id]:
                continue

            properties = tuple(DBProperty(rel_map["properties"].get(prop.name, prop.name), prop.value)
                               for prop in rel.properties) if rel.properties else tuple()

            rel = DBRelation(source_id, target_id, rel_map["new_relation_type"], properties)

            if rel.target_id == concept.id_:
                in_relations.append(rel)
            elif rel.source_id == concept.id_:
                out_relations.append(rel)
            else:
                raise ValueError

        return in_relations, out_relations

    @classmethod
    def from_config(cls, reader: AbstractConceptReader, json_config: dict):
        concepts_map = {}
        properties_map = {}

        for old_type, new_type_with_props in json_config["concepts_types_mapping"].items():
            concepts_map[old_type] = new_type_with_props["name"]
            properties_map[old_type] = new_type_with_props.get("properties", {})

        relations_map = {}
        for obj in json_config.get("relations_types_mapping", []):
            relations_map[obj["old_relation_type"]] = {
                "source_type": obj["source_type"],
                "target_type": obj["target_type"],
                "new_relation_type": obj["new_relation_type"],
                "flip_relation": obj.get("flip_relation", False),
                "properties": obj.get("properties", {})
            }

        return cls(reader, concepts_map, relations_map, properties_map)
