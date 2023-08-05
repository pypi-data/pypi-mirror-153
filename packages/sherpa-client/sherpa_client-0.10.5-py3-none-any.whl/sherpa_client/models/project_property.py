from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectProperty")


@attr.s(auto_attribs=True)
class ProjectProperty:
    """
    Attributes:
        name (Union[Unset, str]):  Default: 'value'.
    """

    name: Union[Unset, str] = "value"

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        project_property = cls(
            name=name,
        )

        return project_property
