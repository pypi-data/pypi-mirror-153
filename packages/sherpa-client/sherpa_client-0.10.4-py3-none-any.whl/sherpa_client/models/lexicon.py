from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Lexicon")


@attr.s(auto_attribs=True)
class Lexicon:
    """
    Attributes:
        color (str):
        label (str):
        manual_edition_allowed (bool): (unstable)
        name (str):
        created_at (Union[Unset, str]):
        created_by (Union[Unset, str]):
        modified_at (Union[Unset, str]):
        modified_by (Union[Unset, str]):
        terms (Union[Unset, int]):
    """

    color: str
    label: str
    manual_edition_allowed: bool
    name: str
    created_at: Union[Unset, str] = UNSET
    created_by: Union[Unset, str] = UNSET
    modified_at: Union[Unset, str] = UNSET
    modified_by: Union[Unset, str] = UNSET
    terms: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        color = self.color
        label = self.label
        manual_edition_allowed = self.manual_edition_allowed
        name = self.name
        created_at = self.created_at
        created_by = self.created_by
        modified_at = self.modified_at
        modified_by = self.modified_by
        terms = self.terms

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "color": color,
                "label": label,
                "manualEditionAllowed": manual_edition_allowed,
                "name": name,
            }
        )
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if modified_by is not UNSET:
            field_dict["modifiedBy"] = modified_by
        if terms is not UNSET:
            field_dict["terms"] = terms

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        color = d.pop("color")

        label = d.pop("label")

        manual_edition_allowed = d.pop("manualEditionAllowed")

        name = d.pop("name")

        created_at = d.pop("createdAt", UNSET)

        created_by = d.pop("createdBy", UNSET)

        modified_at = d.pop("modifiedAt", UNSET)

        modified_by = d.pop("modifiedBy", UNSET)

        terms = d.pop("terms", UNSET)

        lexicon = cls(
            color=color,
            label=label,
            manual_edition_allowed=manual_edition_allowed,
            name=name,
            created_at=created_at,
            created_by=created_by,
            modified_at=modified_at,
            modified_by=modified_by,
            terms=terms,
        )

        return lexicon
