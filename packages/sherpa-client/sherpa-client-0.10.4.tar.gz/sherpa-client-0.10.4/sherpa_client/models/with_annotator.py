from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.with_annotator_condition import WithAnnotatorCondition
from ..models.with_annotator_parameters import WithAnnotatorParameters
from ..types import UNSET, Unset

T = TypeVar("T", bound="WithAnnotator")


@attr.s(auto_attribs=True)
class WithAnnotator:
    """
    Attributes:
        annotator (str):
        condition (Union[Unset, WithAnnotatorCondition]):
        disabled (Union[Unset, bool]):
        parameters (Union[Unset, WithAnnotatorParameters]):
        project_name (Union[Unset, str]):
    """

    annotator: str
    condition: Union[Unset, WithAnnotatorCondition] = UNSET
    disabled: Union[Unset, bool] = UNSET
    parameters: Union[Unset, WithAnnotatorParameters] = UNSET
    project_name: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        annotator = self.annotator
        condition: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.condition, Unset):
            condition = self.condition.to_dict()

        disabled = self.disabled
        parameters: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = self.parameters.to_dict()

        project_name = self.project_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "annotator": annotator,
            }
        )
        if condition is not UNSET:
            field_dict["condition"] = condition
        if disabled is not UNSET:
            field_dict["disabled"] = disabled
        if parameters is not UNSET:
            field_dict["parameters"] = parameters
        if project_name is not UNSET:
            field_dict["projectName"] = project_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        annotator = d.pop("annotator")

        _condition = d.pop("condition", UNSET)
        condition: Union[Unset, WithAnnotatorCondition]
        if isinstance(_condition, Unset):
            condition = UNSET
        else:
            condition = WithAnnotatorCondition.from_dict(_condition)

        disabled = d.pop("disabled", UNSET)

        _parameters = d.pop("parameters", UNSET)
        parameters: Union[Unset, WithAnnotatorParameters]
        if isinstance(_parameters, Unset):
            parameters = UNSET
        else:
            parameters = WithAnnotatorParameters.from_dict(_parameters)

        project_name = d.pop("projectName", UNSET)

        with_annotator = cls(
            annotator=annotator,
            condition=condition,
            disabled=disabled,
            parameters=parameters,
            project_name=project_name,
        )

        return with_annotator
