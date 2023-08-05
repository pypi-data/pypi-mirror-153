from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="DocAltText")


@attr.s(auto_attribs=True)
class DocAltText:
    """A document alternative text

    Attributes:
        name (str): The alternative text name
        text (str): The alternative text
        created_by (Union[Unset, str]): User having created the category
        created_date (Union[Unset, str]): Creation date
        modified_date (Union[Unset, str]): Last modification date
    """

    name: str
    text: str
    created_by: Union[Unset, str] = UNSET
    created_date: Union[Unset, str] = UNSET
    modified_date: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        text = self.text
        created_by = self.created_by
        created_date = self.created_date
        modified_date = self.modified_date

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "text": text,
            }
        )
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if created_date is not UNSET:
            field_dict["createdDate"] = created_date
        if modified_date is not UNSET:
            field_dict["modifiedDate"] = modified_date

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        text = d.pop("text")

        created_by = d.pop("createdBy", UNSET)

        created_date = d.pop("createdDate", UNSET)

        modified_date = d.pop("modifiedDate", UNSET)

        doc_alt_text = cls(
            name=name,
            text=text,
            created_by=created_by,
            created_date=created_date,
            modified_date=modified_date,
        )

        return doc_alt_text
