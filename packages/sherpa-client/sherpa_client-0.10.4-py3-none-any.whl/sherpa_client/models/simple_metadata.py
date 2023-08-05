from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="SimpleMetadata")


@attr.s(auto_attribs=True)
class SimpleMetadata:
    """
    Attributes:
        name (str):
        value (Union[Unset, str]):
    """

    name: str
    value: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
            }
        )
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        value = d.pop("value", UNSET)

        simple_metadata = cls(
            name=name,
            value=value,
        )

        return simple_metadata
