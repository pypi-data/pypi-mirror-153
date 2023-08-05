from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="CreatedByCount")


@attr.s(auto_attribs=True)
class CreatedByCount:
    """
    Attributes:
        count (int):
        created_by (str):
    """

    count: int
    created_by: str

    def to_dict(self) -> Dict[str, Any]:
        count = self.count
        created_by = self.created_by

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "count": count,
                "createdBy": created_by,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        count = d.pop("count")

        created_by = d.pop("createdBy")

        created_by_count = cls(
            count=count,
            created_by=created_by,
        )

        return created_by_count
