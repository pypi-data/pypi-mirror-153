from typing import Any, Dict, Type, TypeVar

import attr

from ..models.segment import Segment

T = TypeVar("T", bound="SegmentHit")


@attr.s(auto_attribs=True)
class SegmentHit:
    """
    Attributes:
        id (str):
        score (float):
        segment (Segment):
    """

    id: str
    score: float
    segment: Segment

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        score = self.score
        segment = self.segment.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "_id": id,
                "score": score,
                "segment": segment,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("_id")

        score = d.pop("score")

        segment = Segment.from_dict(d.pop("segment"))

        segment_hit = cls(
            id=id,
            score=score,
            segment=segment,
        )

        return segment_hit
