from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="ShareMode")


@attr.s(auto_attribs=True)
class ShareMode:
    """
    Attributes:
        read (bool):
        write (bool):
    """

    read: bool
    write: bool

    def to_dict(self) -> Dict[str, Any]:
        read = self.read
        write = self.write

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "read": read,
                "write": write,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        read = d.pop("read")

        write = d.pop("write")

        share_mode = cls(
            read=read,
            write=write,
        )

        return share_mode
