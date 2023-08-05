from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="GroupDesc")


@attr.s(auto_attribs=True)
class GroupDesc:
    """
    Attributes:
        label (str):
        max_users (int):
        name (str):
        attached_roles (Union[Unset, List[str]]):
        created_at (Union[Unset, str]):
        created_by (Union[Unset, str]):
        modified_at (Union[Unset, str]):
        modified_by (Union[Unset, str]):
    """

    label: str
    max_users: int
    name: str
    attached_roles: Union[Unset, List[str]] = UNSET
    created_at: Union[Unset, str] = UNSET
    created_by: Union[Unset, str] = UNSET
    modified_at: Union[Unset, str] = UNSET
    modified_by: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        label = self.label
        max_users = self.max_users
        name = self.name
        attached_roles: Union[Unset, List[str]] = UNSET
        if not isinstance(self.attached_roles, Unset):
            attached_roles = self.attached_roles

        created_at = self.created_at
        created_by = self.created_by
        modified_at = self.modified_at
        modified_by = self.modified_by

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "label": label,
                "maxUsers": max_users,
                "name": name,
            }
        )
        if attached_roles is not UNSET:
            field_dict["attachedRoles"] = attached_roles
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if modified_by is not UNSET:
            field_dict["modifiedBy"] = modified_by

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        label = d.pop("label")

        max_users = d.pop("maxUsers")

        name = d.pop("name")

        attached_roles = cast(List[str], d.pop("attachedRoles", UNSET))

        created_at = d.pop("createdAt", UNSET)

        created_by = d.pop("createdBy", UNSET)

        modified_at = d.pop("modifiedAt", UNSET)

        modified_by = d.pop("modifiedBy", UNSET)

        group_desc = cls(
            label=label,
            max_users=max_users,
            name=name,
            attached_roles=attached_roles,
            created_at=created_at,
            created_by=created_by,
            modified_at=modified_at,
            modified_by=modified_by,
        )

        return group_desc
