from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PartialLexicon")


@attr.s(auto_attribs=True)
class PartialLexicon:
    """
    Attributes:
        label (str):
        color (Union[Unset, str]):
        name (Union[Unset, str]):
    """

    label: str
    color: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        label = self.label
        color = self.color
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "label": label,
            }
        )
        if color is not UNSET:
            field_dict["color"] = color
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        label = d.pop("label")

        color = d.pop("color", UNSET)

        name = d.pop("name", UNSET)

        partial_lexicon = cls(
            label=label,
            color=color,
            name=name,
        )

        return partial_lexicon
