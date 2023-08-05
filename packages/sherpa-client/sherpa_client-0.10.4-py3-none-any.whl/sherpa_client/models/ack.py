from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="Ack")


@attr.s(auto_attribs=True)
class Ack:
    """
    Attributes:
        ok (bool):
    """

    ok: bool

    def to_dict(self) -> Dict[str, Any]:
        ok = self.ok

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "ok": ok,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        ok = d.pop("ok")

        ack = cls(
            ok=ok,
        )

        return ack
