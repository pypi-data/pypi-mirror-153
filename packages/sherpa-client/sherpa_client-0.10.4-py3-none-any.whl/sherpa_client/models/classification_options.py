from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ClassificationOptions")


@attr.s(auto_attribs=True)
class ClassificationOptions:
    """
    Attributes:
        exclusive_classes (Union[Unset, bool]):  Default: True.
    """

    exclusive_classes: Union[Unset, bool] = True

    def to_dict(self) -> Dict[str, Any]:
        exclusive_classes = self.exclusive_classes

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if exclusive_classes is not UNSET:
            field_dict["exclusive_classes"] = exclusive_classes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        exclusive_classes = d.pop("exclusive_classes", UNSET)

        classification_options = cls(
            exclusive_classes=exclusive_classes,
        )

        return classification_options
