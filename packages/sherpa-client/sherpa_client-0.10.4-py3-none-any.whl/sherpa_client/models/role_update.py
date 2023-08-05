from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="RoleUpdate")


@attr.s(auto_attribs=True)
class RoleUpdate:
    """
    Attributes:
        label (Union[Unset, str]):
        permissions (Union[Unset, List[str]]):
    """

    label: Union[Unset, str] = UNSET
    permissions: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        label = self.label
        permissions: Union[Unset, List[str]] = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = self.permissions

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if label is not UNSET:
            field_dict["label"] = label
        if permissions is not UNSET:
            field_dict["permissions"] = permissions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        label = d.pop("label", UNSET)

        permissions = cast(List[str], d.pop("permissions", UNSET))

        role_update = cls(
            label=label,
            permissions=permissions,
        )

        return role_update
