from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="NewRole")


@attr.s(auto_attribs=True)
class NewRole:
    """
    Attributes:
        label (str):
        permissions (List[str]):
    """

    label: str
    permissions: List[str]

    def to_dict(self) -> Dict[str, Any]:
        label = self.label
        permissions = self.permissions

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "label": label,
                "permissions": permissions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        label = d.pop("label")

        permissions = cast(List[str], d.pop("permissions"))

        new_role = cls(
            label=label,
            permissions=permissions,
        )

        return new_role
