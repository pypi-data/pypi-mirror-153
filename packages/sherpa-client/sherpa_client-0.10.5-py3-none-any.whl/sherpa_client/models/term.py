from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="Term")


@attr.s(auto_attribs=True)
class Term:
    """
    Attributes:
        identifier (str):
    """

    identifier: str

    def to_dict(self) -> Dict[str, Any]:
        identifier = self.identifier

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "identifier": identifier,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        identifier = d.pop("identifier")

        term = cls(
            identifier=identifier,
        )

        return term
