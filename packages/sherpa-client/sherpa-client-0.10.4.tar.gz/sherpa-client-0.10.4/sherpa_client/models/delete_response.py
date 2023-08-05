from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.sherpa_job_bean import SherpaJobBean
from ..types import UNSET, Unset

T = TypeVar("T", bound="DeleteResponse")


@attr.s(auto_attribs=True)
class DeleteResponse:
    """
    Attributes:
        removed_count (int):
        remove_job (Union[Unset, SherpaJobBean]):
    """

    removed_count: int
    remove_job: Union[Unset, SherpaJobBean] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        removed_count = self.removed_count
        remove_job: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.remove_job, Unset):
            remove_job = self.remove_job.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "removedCount": removed_count,
            }
        )
        if remove_job is not UNSET:
            field_dict["removeJob"] = remove_job

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        removed_count = d.pop("removedCount")

        _remove_job = d.pop("removeJob", UNSET)
        remove_job: Union[Unset, SherpaJobBean]
        if isinstance(_remove_job, Unset):
            remove_job = UNSET
        else:
            remove_job = SherpaJobBean.from_dict(_remove_job)

        delete_response = cls(
            removed_count=removed_count,
            remove_job=remove_job,
        )

        return delete_response
