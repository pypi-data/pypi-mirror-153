from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="GeneratedLabelHint")


@attr.s(auto_attribs=True)
class GeneratedLabelHint:
    """
    Attributes:
        label_hint (str):
    """

    label_hint: str

    def to_dict(self) -> Dict[str, Any]:
        label_hint = self.label_hint

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "labelHint": label_hint,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        label_hint = d.pop("labelHint")

        generated_label_hint = cls(
            label_hint=label_hint,
        )

        return generated_label_hint
