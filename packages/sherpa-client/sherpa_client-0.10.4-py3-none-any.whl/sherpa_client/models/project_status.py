from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.sherpa_job_bean import SherpaJobBean
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectStatus")


@attr.s(auto_attribs=True)
class ProjectStatus:
    """
    Attributes:
        project_name (str):
        status (str):
        pending_job (Union[Unset, SherpaJobBean]):
    """

    project_name: str
    status: str
    pending_job: Union[Unset, SherpaJobBean] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        project_name = self.project_name
        status = self.status
        pending_job: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pending_job, Unset):
            pending_job = self.pending_job.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "projectName": project_name,
                "status": status,
            }
        )
        if pending_job is not UNSET:
            field_dict["pendingJob"] = pending_job

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        project_name = d.pop("projectName")

        status = d.pop("status")

        _pending_job = d.pop("pendingJob", UNSET)
        pending_job: Union[Unset, SherpaJobBean]
        if isinstance(_pending_job, Unset):
            pending_job = UNSET
        else:
            pending_job = SherpaJobBean.from_dict(_pending_job)

        project_status = cls(
            project_name=project_name,
            status=status,
            pending_job=pending_job,
        )

        return project_status
