from typing import Any, Dict, Type, TypeVar

import attr

from ..models.new_experiment_parameters import NewExperimentParameters

T = TypeVar("T", bound="NewExperiment")


@attr.s(auto_attribs=True)
class NewExperiment:
    """
    Attributes:
        engine (str):
        label (str):
        parameters (NewExperimentParameters):
    """

    engine: str
    label: str
    parameters: NewExperimentParameters

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

        parameters = NewExperimentParameters.from_dict(d.pop("parameters"))

        new_experiment = cls(
            engine=engine,
            label=label,
            parameters=parameters,
        )

        return new_experiment
