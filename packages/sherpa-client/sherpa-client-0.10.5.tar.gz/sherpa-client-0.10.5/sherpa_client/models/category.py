from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.category_status import CategoryStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="Category")


@attr.s(auto_attribs=True)
class Category:
    """A document category

    Attributes:
        document_identifier (str): identifier of the document
        label_name (str): The label name
        score (Union[Unset, float]): Score of the category
        status (Union[Unset, CategoryStatus]): Status of the category
    """

    document_identifier: str
    label_name: str
    score: Union[Unset, float] = UNSET
    status: Union[Unset, CategoryStatus] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        document_identifier = self.document_identifier
        label_name = self.label_name
        score = self.score
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "documentIdentifier": document_identifier,
                "labelName": label_name,
            }
        )
        if score is not UNSET:
            field_dict["score"] = score
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        document_identifier = d.pop("documentIdentifier")

        label_name = d.pop("labelName")

        score = d.pop("score", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, CategoryStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = CategoryStatus(_status)

        category = cls(
            document_identifier=document_identifier,
            label_name=label_name,
            score=score,
            status=status,
        )

        return category
