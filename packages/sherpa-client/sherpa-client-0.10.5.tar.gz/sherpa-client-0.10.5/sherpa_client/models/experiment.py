from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.experiment_parameters import ExperimentParameters
from ..models.report import Report
from ..types import UNSET, Unset

T = TypeVar("T", bound="Experiment")


@attr.s(auto_attribs=True)
class Experiment:
    """
    Attributes:
        duration (int):
        engine (str):
        label (str):
        models (int):
        name (str):
        parameters (ExperimentParameters):
        quality (int):
        running (bool):
        timestamp (int):
        uptodate (bool):
        favorite (Union[Unset, bool]):
        report (Union[Unset, Report]):
    """

    duration: int
    engine: str
    label: str
    models: int
    name: str
    parameters: ExperimentParameters
    quality: int
    running: bool
    timestamp: int
    uptodate: bool
    favorite: Union[Unset, bool] = UNSET
    report: Union[Unset, Report] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        duration = self.duration
        engine = self.engine
        label = self.label
        models = self.models
        name = self.name
        parameters = self.parameters.to_dict()

        quality = self.quality
        running = self.running
        timestamp = self.timestamp
        uptodate = self.uptodate
        favorite = self.favorite
        report: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.report, Unset):
            report = self.report.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "duration": duration,
                "engine": engine,
                "label": label,
                "models": models,
                "name": name,
                "parameters": parameters,
                "quality": quality,
                "running": running,
                "timestamp": timestamp,
                "uptodate": uptodate,
            }
        )
        if favorite is not UNSET:
            field_dict["favorite"] = favorite
        if report is not UNSET:
            field_dict["report"] = report

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        duration = d.pop("duration")

        engine = d.pop("engine")

        label = d.pop("label")

        models = d.pop("models")

        name = d.pop("name")

        parameters = ExperimentParameters.from_dict(d.pop("parameters"))

        quality = d.pop("quality")

        running = d.pop("running")

        timestamp = d.pop("timestamp")

        uptodate = d.pop("uptodate")

        favorite = d.pop("favorite", UNSET)

        _report = d.pop("report", UNSET)
        report: Union[Unset, Report]
        if isinstance(_report, Unset):
            report = UNSET
        else:
            report = Report.from_dict(_report)

        experiment = cls(
            duration=duration,
            engine=engine,
            label=label,
            models=models,
            name=name,
            parameters=parameters,
            quality=quality,
            running=running,
            timestamp=timestamp,
            uptodate=uptodate,
            favorite=favorite,
            report=report,
        )

        return experiment
