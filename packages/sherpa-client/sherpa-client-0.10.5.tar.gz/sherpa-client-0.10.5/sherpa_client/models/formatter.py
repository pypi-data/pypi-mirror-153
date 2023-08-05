from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.formatter_parameters import FormatterParameters
from ..types import UNSET, Unset

T = TypeVar("T", bound="Formatter")


@attr.s(auto_attribs=True)
class Formatter:
    """
    Attributes:
        name (str): Name of the formatter (e.g. tabular)
        parameters (Union[Unset, FormatterParameters]): Optional formatting parameters
    """

    name: str
    parameters: Union[Unset, FormatterParameters] = UNSET

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
        parameters: Union[Unset, FormatterParameters]
        if isinstance(_parameters, Unset):
            parameters = UNSET
        else:
            parameters = FormatterParameters.from_dict(_parameters)

        formatter = cls(
            name=name,
            parameters=parameters,
        )

        return formatter
