from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.suggester_patch_parameters import SuggesterPatchParameters
from ..types import UNSET, Unset

T = TypeVar("T", bound="SuggesterPatch")


@attr.s(auto_attribs=True)
class SuggesterPatch:
    """
    Attributes:
        label (Union[Unset, str]):
        parameters (Union[Unset, SuggesterPatchParameters]):
    """

    label: Union[Unset, str] = UNSET
    parameters: Union[Unset, SuggesterPatchParameters] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        label = self.label
        parameters: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = self.parameters.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if label is not UNSET:
            field_dict["label"] = label
        if parameters is not UNSET:
            field_dict["parameters"] = parameters

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        label = d.pop("label", UNSET)

        _parameters = d.pop("parameters", UNSET)
        parameters: Union[Unset, SuggesterPatchParameters]
        if isinstance(_parameters, Unset):
            parameters = UNSET
        else:
            parameters = SuggesterPatchParameters.from_dict(_parameters)

        suggester_patch = cls(
            label=label,
            parameters=parameters,
        )

        return suggester_patch
