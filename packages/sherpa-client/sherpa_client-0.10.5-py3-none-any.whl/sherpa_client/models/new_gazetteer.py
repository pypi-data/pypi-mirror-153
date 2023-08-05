from typing import Any, Dict, Type, TypeVar

import attr

from ..models.new_gazetteer_parameters import NewGazetteerParameters

T = TypeVar("T", bound="NewGazetteer")


@attr.s(auto_attribs=True)
class NewGazetteer:
    """
    Attributes:
        engine (str):
        label (str):
        parameters (NewGazetteerParameters):
    """

    engine: str
    label: str
    parameters: NewGazetteerParameters

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

        parameters = NewGazetteerParameters.from_dict(d.pop("parameters"))

        new_gazetteer = cls(
            engine=engine,
            label=label,
            parameters=parameters,
        )

        return new_gazetteer
