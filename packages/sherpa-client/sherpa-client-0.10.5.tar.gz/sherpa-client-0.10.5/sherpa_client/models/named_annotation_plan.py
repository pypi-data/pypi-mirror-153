from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.annotation_plan import AnnotationPlan
from ..types import UNSET, Unset

T = TypeVar("T", bound="NamedAnnotationPlan")


@attr.s(auto_attribs=True)
class NamedAnnotationPlan:
    """
    Attributes:
        label (str):
        name (str):
        parameters (AnnotationPlan):
        created_at (Union[Unset, str]):
        created_by (Union[Unset, str]):
        favorite (Union[Unset, bool]):
        modified_at (Union[Unset, str]):
        modified_by (Union[Unset, str]):
    """

    label: str
    name: str
    parameters: AnnotationPlan
    created_at: Union[Unset, str] = UNSET
    created_by: Union[Unset, str] = UNSET
    favorite: Union[Unset, bool] = UNSET
    modified_at: Union[Unset, str] = UNSET
    modified_by: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        label = self.label
        name = self.name
        parameters = self.parameters.to_dict()

        created_at = self.created_at
        created_by = self.created_by
        favorite = self.favorite
        modified_at = self.modified_at
        modified_by = self.modified_by

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "label": label,
                "name": name,
                "parameters": parameters,
            }
        )
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if favorite is not UNSET:
            field_dict["favorite"] = favorite
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if modified_by is not UNSET:
            field_dict["modifiedBy"] = modified_by

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        label = d.pop("label")

        name = d.pop("name")

        parameters = AnnotationPlan.from_dict(d.pop("parameters"))

        created_at = d.pop("createdAt", UNSET)

        created_by = d.pop("createdBy", UNSET)

        favorite = d.pop("favorite", UNSET)

        modified_at = d.pop("modifiedAt", UNSET)

        modified_by = d.pop("modifiedBy", UNSET)

        named_annotation_plan = cls(
            label=label,
            name=name,
            parameters=parameters,
            created_at=created_at,
            created_by=created_by,
            favorite=favorite,
            modified_at=modified_at,
            modified_by=modified_by,
        )

        return named_annotation_plan
