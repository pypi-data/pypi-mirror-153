from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="NewGroupDesc")


@attr.s(auto_attribs=True)
class NewGroupDesc:
    """
    Attributes:
        label (str):
        attached_roles (Union[Unset, List[str]]):
        max_users (Union[Unset, int]):
    """

    label: str
    attached_roles: Union[Unset, List[str]] = UNSET
    max_users: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        label = self.label
        attached_roles: Union[Unset, List[str]] = UNSET
        if not isinstance(self.attached_roles, Unset):
            attached_roles = self.attached_roles

        max_users = self.max_users

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "label": label,
            }
        )
        if attached_roles is not UNSET:
            field_dict["attachedRoles"] = attached_roles
        if max_users is not UNSET:
            field_dict["maxUsers"] = max_users

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        label = d.pop("label")

        attached_roles = cast(List[str], d.pop("attachedRoles", UNSET))

        max_users = d.pop("maxUsers", UNSET)

        new_group_desc = cls(
            label=label,
            attached_roles=attached_roles,
            max_users=max_users,
        )

        return new_group_desc
