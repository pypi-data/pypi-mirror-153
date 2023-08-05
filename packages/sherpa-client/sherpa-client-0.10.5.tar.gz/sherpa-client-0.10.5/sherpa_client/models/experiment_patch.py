from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.experiment_patch_parameters import ExperimentPatchParameters
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExperimentPatch")


@attr.s(auto_attribs=True)
class ExperimentPatch:
    """
    Attributes:
        favorite (Union[Unset, bool]):
        label (Union[Unset, str]):
        parameters (Union[Unset, ExperimentPatchParameters]):
    """

    favorite: Union[Unset, bool] = UNSET
    label: Union[Unset, str] = UNSET
    parameters: Union[Unset, ExperimentPatchParameters] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        favorite = self.favorite
        label = self.label
        parameters: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = self.parameters.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if favorite is not UNSET:
            field_dict["favorite"] = favorite
        if label is not UNSET:
            field_dict["label"] = label
        if parameters is not UNSET:
            field_dict["parameters"] = parameters

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        favorite = d.pop("favorite", UNSET)

        label = d.pop("label", UNSET)

        _parameters = d.pop("parameters", UNSET)
        parameters: Union[Unset, ExperimentPatchParameters]
        if isinstance(_parameters, Unset):
            parameters = UNSET
        else:
            parameters = ExperimentPatchParameters.from_dict(_parameters)

        experiment_patch = cls(
            favorite=favorite,
            label=label,
            parameters=parameters,
        )

        return experiment_patch
