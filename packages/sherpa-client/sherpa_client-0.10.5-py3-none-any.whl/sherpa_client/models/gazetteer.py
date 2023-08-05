from typing import Any, Dict, Type, TypeVar

import attr

from ..models.gazetteer_parameters import GazetteerParameters

T = TypeVar("T", bound="Gazetteer")


@attr.s(auto_attribs=True)
class Gazetteer:
    """
    Attributes:
        duration (int):
        engine (str):
        label (str):
        models (int):
        name (str):
        parameters (GazetteerParameters):
        running (bool):
        timestamp (int):
        uptodate (bool):
    """

    duration: int
    engine: str
    label: str
    models: int
    name: str
    parameters: GazetteerParameters
    running: bool
    timestamp: int
    uptodate: bool

    def to_dict(self) -> Dict[str, Any]:
        duration = self.duration
        engine = self.engine
        label = self.label
        models = self.models
        name = self.name
        parameters = self.parameters.to_dict()

        running = self.running
        timestamp = self.timestamp
        uptodate = self.uptodate

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "duration": duration,
                "engine": engine,
                "label": label,
                "models": models,
                "name": name,
                "parameters": parameters,
                "running": running,
                "timestamp": timestamp,
                "uptodate": uptodate,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        duration = d.pop("duration")

        engine = d.pop("engine")

        label = d.pop("label")

        models = d.pop("models")

        name = d.pop("name")

        parameters = GazetteerParameters.from_dict(d.pop("parameters"))

        running = d.pop("running")

        timestamp = d.pop("timestamp")

        uptodate = d.pop("uptodate")

        gazetteer = cls(
            duration=duration,
            engine=engine,
            label=label,
            models=models,
            name=name,
            parameters=parameters,
            running=running,
            timestamp=timestamp,
            uptodate=uptodate,
        )

        return gazetteer
