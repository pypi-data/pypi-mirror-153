from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="LabelUpdate")


@attr.s(auto_attribs=True)
class LabelUpdate:
    """
    Attributes:
        color (Union[Unset, str]):
        identifier (Union[Unset, str]):
        label (Union[Unset, str]):
    """

    color: Union[Unset, str] = UNSET
    identifier: Union[Unset, str] = UNSET
    label: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        color = self.color
        identifier = self.identifier
        label = self.label

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if color is not UNSET:
            field_dict["color"] = color
        if identifier is not UNSET:
            field_dict["identifier"] = identifier
        if label is not UNSET:
            field_dict["label"] = label

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        color = d.pop("color", UNSET)

        identifier = d.pop("identifier", UNSET)

        label = d.pop("label", UNSET)

        label_update = cls(
            color=color,
            identifier=identifier,
            label=label,
        )

        return label_update
