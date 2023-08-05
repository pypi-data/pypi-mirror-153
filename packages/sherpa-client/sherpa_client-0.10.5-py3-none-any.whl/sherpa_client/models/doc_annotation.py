from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.doc_annotation_status import DocAnnotationStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="DocAnnotation")


@attr.s(auto_attribs=True)
class DocAnnotation:
    """A document annotation

    Attributes:
        end (int): End offset in document
        label_name (str): The label name
        start (int): Start offset in document
        text (str): Covered text
        created_by (Union[Unset, str]): User having created the annotation
        created_date (Union[Unset, str]): Creation date
        identifier (Union[Unset, str]): Annotation identifier (only in 'html version')
        modified_date (Union[Unset, str]): Last modification date
        status (Union[Unset, DocAnnotationStatus]): Status of the annotation
    """

    end: int
    label_name: str
    start: int
    text: str
    created_by: Union[Unset, str] = UNSET
    created_date: Union[Unset, str] = UNSET
    identifier: Union[Unset, str] = UNSET
    modified_date: Union[Unset, str] = UNSET
    status: Union[Unset, DocAnnotationStatus] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        end = self.end
        label_name = self.label_name
        start = self.start
        text = self.text
        created_by = self.created_by
        created_date = self.created_date
        identifier = self.identifier
        modified_date = self.modified_date
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "end": end,
                "labelName": label_name,
                "start": start,
                "text": text,
            }
        )
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if created_date is not UNSET:
            field_dict["createdDate"] = created_date
        if identifier is not UNSET:
            field_dict["identifier"] = identifier
        if modified_date is not UNSET:
            field_dict["modifiedDate"] = modified_date
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        end = d.pop("end")

        label_name = d.pop("labelName")

        start = d.pop("start")

        text = d.pop("text")

        created_by = d.pop("createdBy", UNSET)

        created_date = d.pop("createdDate", UNSET)

        identifier = d.pop("identifier", UNSET)

        modified_date = d.pop("modifiedDate", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, DocAnnotationStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = DocAnnotationStatus(_status)

        doc_annotation = cls(
            end=end,
            label_name=label_name,
            start=start,
            text=text,
            created_by=created_by,
            created_date=created_date,
            identifier=identifier,
            modified_date=modified_date,
            status=status,
        )

        return doc_annotation
