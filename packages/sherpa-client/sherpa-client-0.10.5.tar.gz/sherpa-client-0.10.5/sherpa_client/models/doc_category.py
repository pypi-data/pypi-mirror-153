from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.doc_category_status import DocCategoryStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="DocCategory")


@attr.s(auto_attribs=True)
class DocCategory:
    """A document category

    Attributes:
        identifier (str): Category identifier
        label_name (str): The label name
        created_by (Union[Unset, str]): User having created the category
        created_date (Union[Unset, str]): Creation date
        modified_date (Union[Unset, str]): Last modification date
        score (Union[Unset, float]): Score of the category
        status (Union[Unset, DocCategoryStatus]): Status of the category
    """

    identifier: str
    label_name: str
    created_by: Union[Unset, str] = UNSET
    created_date: Union[Unset, str] = UNSET
    modified_date: Union[Unset, str] = UNSET
    score: Union[Unset, float] = UNSET
    status: Union[Unset, DocCategoryStatus] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        identifier = self.identifier
        label_name = self.label_name
        created_by = self.created_by
        created_date = self.created_date
        modified_date = self.modified_date
        score = self.score
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "identifier": identifier,
                "labelName": label_name,
            }
        )
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if created_date is not UNSET:
            field_dict["createdDate"] = created_date
        if modified_date is not UNSET:
            field_dict["modifiedDate"] = modified_date
        if score is not UNSET:
            field_dict["score"] = score
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        identifier = d.pop("identifier")

        label_name = d.pop("labelName")

        created_by = d.pop("createdBy", UNSET)

        created_date = d.pop("createdDate", UNSET)

        modified_date = d.pop("modifiedDate", UNSET)

        score = d.pop("score", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, DocCategoryStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = DocCategoryStatus(_status)

        doc_category = cls(
            identifier=identifier,
            label_name=label_name,
            created_by=created_by,
            created_date=created_date,
            modified_date=modified_date,
            score=score,
            status=status,
        )

        return doc_category
