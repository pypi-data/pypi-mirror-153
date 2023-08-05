from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="InputLabel")


@attr.s(auto_attribs=True)
class InputLabel:
    """
    Attributes:
        label (str):
    """

    label: str

    def to_dict(self) -> Dict[str, Any]:
        label = self.label

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "label": label,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        label = d.pop("label")

        input_label = cls(
            label=label,
        )

        return input_label
