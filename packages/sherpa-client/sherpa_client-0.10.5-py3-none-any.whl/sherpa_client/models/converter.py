from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.converter_parameters import ConverterParameters
from ..types import UNSET, Unset

T = TypeVar("T", bound="Converter")


@attr.s(auto_attribs=True)
class Converter:
    """
    Attributes:
        name (str): Name of the converter (e.g. tika)
        parameters (Union[Unset, ConverterParameters]): Optional conversion parameters
    """

    name: str
    parameters: Union[Unset, ConverterParameters] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        parameters: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = self.parameters.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
            }
        )
        if parameters is not UNSET:
            field_dict["parameters"] = parameters

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        _parameters = d.pop("parameters", UNSET)
        parameters: Union[Unset, ConverterParameters]
        if isinstance(_parameters, Unset):
            parameters = UNSET
        else:
            parameters = ConverterParameters.from_dict(_parameters)

        converter = cls(
            name=name,
            parameters=parameters,
        )

        return converter
