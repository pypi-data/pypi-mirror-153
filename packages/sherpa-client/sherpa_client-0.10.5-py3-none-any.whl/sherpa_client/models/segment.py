from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.doc_annotation import DocAnnotation
from ..models.segment_metadata import SegmentMetadata
from ..types import UNSET, Unset

T = TypeVar("T", bound="Segment")


@attr.s(auto_attribs=True)
class Segment:
    """
    Attributes:
        document_identifier (str):
        document_title (str):
        end (int):
        identifier (str):
        start (int):
        text (str):
        annotations (Union[Unset, List[DocAnnotation]]):
        created_by (Union[Unset, str]): User having created the segment
        created_date (Union[Unset, str]): Creation date
        metadata (Union[Unset, SegmentMetadata]):
        modified_date (Union[Unset, str]): Last modification date
        shift (Union[Unset, int]):
    """

    document_identifier: str
    document_title: str
    end: int
    identifier: str
    start: int
    text: str
    annotations: Union[Unset, List[DocAnnotation]] = UNSET
    created_by: Union[Unset, str] = UNSET
    created_date: Union[Unset, str] = UNSET
    metadata: Union[Unset, SegmentMetadata] = UNSET
    modified_date: Union[Unset, str] = UNSET
    shift: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        document_identifier = self.document_identifier
        document_title = self.document_title
        end = self.end
        identifier = self.identifier
        start = self.start
        text = self.text
        annotations: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.annotations, Unset):
            annotations = []
            for annotations_item_data in self.annotations:
                annotations_item = annotations_item_data.to_dict()

                annotations.append(annotations_item)

        created_by = self.created_by
        created_date = self.created_date
        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        modified_date = self.modified_date
        shift = self.shift

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "documentIdentifier": document_identifier,
                "documentTitle": document_title,
                "end": end,
                "identifier": identifier,
                "start": start,
                "text": text,
            }
        )
        if annotations is not UNSET:
            field_dict["annotations"] = annotations
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if created_date is not UNSET:
            field_dict["createdDate"] = created_date
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if modified_date is not UNSET:
            field_dict["modifiedDate"] = modified_date
        if shift is not UNSET:
            field_dict["shift"] = shift

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        document_identifier = d.pop("documentIdentifier")

        document_title = d.pop("documentTitle")

        end = d.pop("end")

        identifier = d.pop("identifier")

        start = d.pop("start")

        text = d.pop("text")

        annotations = []
        _annotations = d.pop("annotations", UNSET)
        for annotations_item_data in _annotations or []:
            annotations_item = DocAnnotation.from_dict(annotations_item_data)

            annotations.append(annotations_item)

        created_by = d.pop("createdBy", UNSET)

        created_date = d.pop("createdDate", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, SegmentMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = SegmentMetadata.from_dict(_metadata)

        modified_date = d.pop("modifiedDate", UNSET)

        shift = d.pop("shift", UNSET)

        segment = cls(
            document_identifier=document_identifier,
            document_title=document_title,
            end=end,
            identifier=identifier,
            start=start,
            text=text,
            annotations=annotations,
            created_by=created_by,
            created_date=created_date,
            metadata=metadata,
            modified_date=modified_date,
            shift=shift,
        )

        return segment
