from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="Bucket")


@attr.s(auto_attribs=True)
class Bucket:
    """
    Attributes:
        doc_count (int):
        key (str):
    """

    doc_count: int
    key: str

    def to_dict(self) -> Dict[str, Any]:
        doc_count = self.doc_count
        key = self.key

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "doc_count": doc_count,
                "key": key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        doc_count = d.pop("doc_count")

        key = d.pop("key")

        bucket = cls(
            doc_count=doc_count,
            key=key,
        )

        return bucket
