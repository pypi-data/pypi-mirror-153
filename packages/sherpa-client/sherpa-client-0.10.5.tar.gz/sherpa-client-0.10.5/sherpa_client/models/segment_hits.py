from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.aggregation import Aggregation
from ..models.search_total import SearchTotal
from ..models.segment_hit import SegmentHit
from ..types import UNSET, Unset

T = TypeVar("T", bound="SegmentHits")


@attr.s(auto_attribs=True)
class SegmentHits:
    """
    Attributes:
        hits (List[SegmentHit]):
        total (SearchTotal):
        aggregations (Union[Unset, List[Aggregation]]):
        max_score (Union[Unset, float]):
    """

    hits: List[SegmentHit]
    total: SearchTotal
    aggregations: Union[Unset, List[Aggregation]] = UNSET
    max_score: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        hits = []
        for hits_item_data in self.hits:
            hits_item = hits_item_data.to_dict()

            hits.append(hits_item)

        total = self.total.to_dict()

        aggregations: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.aggregations, Unset):
            aggregations = []
            for aggregations_item_data in self.aggregations:
                aggregations_item = aggregations_item_data.to_dict()

                aggregations.append(aggregations_item)

        max_score = self.max_score

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "hits": hits,
                "total": total,
            }
        )
        if aggregations is not UNSET:
            field_dict["aggregations"] = aggregations
        if max_score is not UNSET:
            field_dict["max_score"] = max_score

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        hits = []
        _hits = d.pop("hits")
        for hits_item_data in _hits:
            hits_item = SegmentHit.from_dict(hits_item_data)

            hits.append(hits_item)

        total = SearchTotal.from_dict(d.pop("total"))

        aggregations = []
        _aggregations = d.pop("aggregations", UNSET)
        for aggregations_item_data in _aggregations or []:
            aggregations_item = Aggregation.from_dict(aggregations_item_data)

            aggregations.append(aggregations_item)

        max_score = d.pop("max_score", UNSET)

        segment_hits = cls(
            hits=hits,
            total=total,
            aggregations=aggregations,
            max_score=max_score,
        )

        return segment_hits
