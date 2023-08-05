from typing import Any, Dict, Type, TypeVar

import attr

from ..models.segment_context import SegmentContext

T = TypeVar("T", bound="SegmentContexts")


@attr.s(auto_attribs=True)
class SegmentContexts:
    """
    Attributes:
        after (SegmentContext):
        before (SegmentContext):
    """

    after: SegmentContext
    before: SegmentContext

    def to_dict(self) -> Dict[str, Any]:
        after = self.after.to_dict()

        before = self.before.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "after": after,
                "before": before,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        after = SegmentContext.from_dict(d.pop("after"))

        before = SegmentContext.from_dict(d.pop("before"))

        segment_contexts = cls(
            after=after,
            before=before,
        )

        return segment_contexts
