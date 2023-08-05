from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Annotator")


@attr.s(auto_attribs=True)
class Annotator:
    """
    Attributes:
        engine (str):
        label (str):
        name (str):
        favorite (Union[Unset, bool]):
        is_default (Union[Unset, bool]):
    """

    engine: str
    label: str
    name: str
    favorite: Union[Unset, bool] = UNSET
    is_default: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        engine = self.engine
        label = self.label
        name = self.name
        favorite = self.favorite
        is_default = self.is_default

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "engine": engine,
                "label": label,
                "name": name,
            }
        )
        if favorite is not UNSET:
            field_dict["favorite"] = favorite
        if is_default is not UNSET:
            field_dict["isDefault"] = is_default

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        engine = d.pop("engine")

        label = d.pop("label")

        name = d.pop("name")

        favorite = d.pop("favorite", UNSET)

        is_default = d.pop("isDefault", UNSET)

        annotator = cls(
            engine=engine,
            label=label,
            name=name,
            favorite=favorite,
            is_default=is_default,
        )

        return annotator
