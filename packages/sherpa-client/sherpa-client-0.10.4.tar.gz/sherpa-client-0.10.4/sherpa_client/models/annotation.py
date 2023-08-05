from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.annotation_status import AnnotationStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="Annotation")


@attr.s(auto_attribs=True)
class Annotation:
    """A document annotation

    Attributes:
        document_identifier (str): The document identifier
        end (int): End offset in document
        label_name (str): The label name
        start (int): Start offset in document
        text (str): Covered text
        status (Union[Unset, AnnotationStatus]): Status of the annotation
    """

    document_identifier: str
    end: int
    label_name: str
    start: int
    text: str
    status: Union[Unset, AnnotationStatus] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        document_identifier = self.document_identifier
        end = self.end
        label_name = self.label_name
        start = self.start
        text = self.text
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "documentIdentifier": document_identifier,
                "end": end,
                "labelName": label_name,
                "start": start,
                "text": text,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        document_identifier = d.pop("documentIdentifier")

        end = d.pop("end")

        label_name = d.pop("labelName")

        start = d.pop("start")

        text = d.pop("text")

        _status = d.pop("status", UNSET)
        status: Union[Unset, AnnotationStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = AnnotationStatus(_status)

        annotation = cls(
            document_identifier=document_identifier,
            end=end,
            label_name=label_name,
            start=start,
            text=text,
            status=status,
        )

        return annotation
