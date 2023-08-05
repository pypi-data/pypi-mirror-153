from typing import Any, Dict, Type, TypeVar

import attr

from ..models.new_suggester_parameters import NewSuggesterParameters

T = TypeVar("T", bound="NewSuggester")


@attr.s(auto_attribs=True)
class NewSuggester:
    """
    Attributes:
        engine (str):
        label (str):
        parameters (NewSuggesterParameters):
    """

    engine: str
    label: str
    parameters: NewSuggesterParameters

    def to_dict(self) -> Dict[str, Any]:
        engine = self.engine
        label = self.label
        parameters = self.parameters.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "engine": engine,
                "label": label,
                "parameters": parameters,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        engine = d.pop("engine")

        label = d.pop("label")

        parameters = NewSuggesterParameters.from_dict(d.pop("parameters"))

        new_suggester = cls(
            engine=engine,
            label=label,
            parameters=parameters,
        )

        return new_suggester
