from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="LexiconUpdate")


@attr.s(auto_attribs=True)
class LexiconUpdate:
    """
    Attributes:
        color (Union[Unset, str]):
        label (Union[Unset, str]):
    """

    color: Union[Unset, str] = UNSET
    label: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        color = self.color
        label = self.label

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if color is not UNSET:
            field_dict["color"] = color
        if label is not UNSET:
            field_dict["label"] = label

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        color = d.pop("color", UNSET)

        label = d.pop("label", UNSET)

        lexicon_update = cls(
            color=color,
            label=label,
        )

        return lexicon_update
