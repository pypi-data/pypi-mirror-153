from typing import Any, Dict, Type, TypeVar

import attr

from ..models.search_total_relation import SearchTotalRelation

T = TypeVar("T", bound="SearchTotal")


@attr.s(auto_attribs=True)
class SearchTotal:
    """
    Attributes:
        relation (SearchTotalRelation):
        value (int):
    """

    relation: SearchTotalRelation
    value: int

    def to_dict(self) -> Dict[str, Any]:
        relation = self.relation.value

        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "relation": relation,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        relation = SearchTotalRelation(d.pop("relation"))

        value = d.pop("value")

        search_total = cls(
            relation=relation,
            value=value,
        )

        return search_total
