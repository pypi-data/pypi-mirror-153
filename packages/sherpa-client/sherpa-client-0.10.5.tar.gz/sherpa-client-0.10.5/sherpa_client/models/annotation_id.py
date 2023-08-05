from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="AnnotationId")


@attr.s(auto_attribs=True)
class AnnotationId:
    """Annotation creation response

    Attributes:
        identifier (str): Identifier of the new annotation
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

        annotation_id = cls(
            identifier=identifier,
        )

        return annotation_id
