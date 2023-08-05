from typing import Any, Dict, Type, TypeVar

import attr

from ..models.annotation_plan import AnnotationPlan

T = TypeVar("T", bound="NewNamedAnnotationPlan")


@attr.s(auto_attribs=True)
class NewNamedAnnotationPlan:
    """
    Attributes:
        label (str):
        parameters (AnnotationPlan):
    """

    label: str
    parameters: AnnotationPlan

    def to_dict(self) -> Dict[str, Any]:
        label = self.label
        parameters = self.parameters.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "label": label,
                "parameters": parameters,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        label = d.pop("label")

        parameters = AnnotationPlan.from_dict(d.pop("parameters"))

        new_named_annotation_plan = cls(
            label=label,
            parameters=parameters,
        )

        return new_named_annotation_plan
