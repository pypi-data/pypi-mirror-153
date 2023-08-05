from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="ClassificationConfig")


@attr.s(auto_attribs=True)
class ClassificationConfig:
    """
    Attributes:
        exclusive_classes (bool):
    """

    exclusive_classes: bool

    def to_dict(self) -> Dict[str, Any]:
        exclusive_classes = self.exclusive_classes

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "exclusive_classes": exclusive_classes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        exclusive_classes = d.pop("exclusive_classes")

        classification_config = cls(
            exclusive_classes=exclusive_classes,
        )

        return classification_config
