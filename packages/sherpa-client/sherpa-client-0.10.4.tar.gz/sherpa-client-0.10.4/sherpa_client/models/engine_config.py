from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="EngineConfig")


@attr.s(auto_attribs=True)
class EngineConfig:
    """
    Attributes:
        name (str):
        type (str):
    """

    name: str
    type: str

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        type = self.type

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "type": type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        type = d.pop("type")

        engine_config = cls(
            name=name,
            type=type,
        )

        return engine_config
