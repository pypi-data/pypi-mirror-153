from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.sherpa_job_bean import SherpaJobBean
from ..types import UNSET, Unset

T = TypeVar("T", bound="EngineConfigImportSummary")


@attr.s(auto_attribs=True)
class EngineConfigImportSummary:
    """
    Attributes:
        configs (Union[Unset, List[str]]):
        ignored (Union[Unset, List[str]]):
        models (Union[Unset, int]): number of models that will be imported
        pending_job (Union[Unset, SherpaJobBean]):
    """

    configs: Union[Unset, List[str]] = UNSET
    ignored: Union[Unset, List[str]] = UNSET
    models: Union[Unset, int] = 0
    pending_job: Union[Unset, SherpaJobBean] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        configs: Union[Unset, List[str]] = UNSET
        if not isinstance(self.configs, Unset):
            configs = self.configs

        ignored: Union[Unset, List[str]] = UNSET
        if not isinstance(self.ignored, Unset):
            ignored = self.ignored

        models = self.models
        pending_job: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pending_job, Unset):
            pending_job = self.pending_job.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if configs is not UNSET:
            field_dict["configs"] = configs
        if ignored is not UNSET:
            field_dict["ignored"] = ignored
        if models is not UNSET:
            field_dict["models"] = models
        if pending_job is not UNSET:
            field_dict["pendingJob"] = pending_job

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        configs = cast(List[str], d.pop("configs", UNSET))

        ignored = cast(List[str], d.pop("ignored", UNSET))

        models = d.pop("models", UNSET)

        _pending_job = d.pop("pendingJob", UNSET)
        pending_job: Union[Unset, SherpaJobBean]
        if isinstance(_pending_job, Unset):
            pending_job = UNSET
        else:
            pending_job = SherpaJobBean.from_dict(_pending_job)

        engine_config_import_summary = cls(
            configs=configs,
            ignored=ignored,
            models=models,
            pending_job=pending_job,
        )

        return engine_config_import_summary
