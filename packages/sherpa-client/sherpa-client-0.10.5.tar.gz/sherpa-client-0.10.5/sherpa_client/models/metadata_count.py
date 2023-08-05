from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="MetadataCount")


@attr.s(auto_attribs=True)
class MetadataCount:
    """
    Attributes:
        id (str):
        document_count (int):
        segment_count (int):
    """

    id: str
    document_count: int
    segment_count: int

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        document_count = self.document_count
        segment_count = self.segment_count

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "_id": id,
                "documentCount": document_count,
                "segmentCount": segment_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("_id")

        document_count = d.pop("documentCount")

        segment_count = d.pop("segmentCount")

        metadata_count = cls(
            id=id,
            document_count=document_count,
            segment_count=segment_count,
        )

        return metadata_count
