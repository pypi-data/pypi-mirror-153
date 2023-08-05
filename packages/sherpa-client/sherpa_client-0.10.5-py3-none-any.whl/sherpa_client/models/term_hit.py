from typing import Any, Dict, Type, TypeVar

import attr

from ..models.term_hit_term import TermHitTerm

T = TypeVar("T", bound="TermHit")


@attr.s(auto_attribs=True)
class TermHit:
    """
    Attributes:
        score (float):
        term (TermHitTerm):
    """

    score: float
    term: TermHitTerm

    def to_dict(self) -> Dict[str, Any]:
        score = self.score
        term = self.term.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "score": score,
                "term": term,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        score = d.pop("score")

        term = TermHitTerm.from_dict(d.pop("term"))

        term_hit = cls(
            score=score,
            term=term,
        )

        return term_hit
