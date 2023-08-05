import json
from io import BytesIO
from typing import Any, Dict, Tuple, Type, TypeVar, Union

import attr

from ..models.convert_annotation_plan import ConvertAnnotationPlan
from ..types import UNSET, File, FileJsonType, Unset

T = TypeVar("T", bound="AnnotateBinaryForm")


@attr.s(auto_attribs=True)
class AnnotateBinaryForm:
    """
    Attributes:
        file (Union[Unset, File]):  binary file to be converted and annotated
        plan (Union[Unset, ConvertAnnotationPlan]):
    """

    file: Union[Unset, File] = UNSET
    plan: Union[Unset, ConvertAnnotationPlan] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        file: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.file, Unset):
            file = self.file.to_tuple()

        plan: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.plan, Unset):
            plan = self.plan.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if file is not UNSET:
            field_dict["file"] = file
        if plan is not UNSET:
            field_dict["plan"] = plan

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        file: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.file, Unset):
            file = self.file.to_tuple()

        plan: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.plan, Unset):
            plan = (None, json.dumps(self.plan.to_dict()).encode(), "application/json")

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if file is not UNSET:
            field_dict["file"] = file
        if plan is not UNSET:
            field_dict["plan"] = plan

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _file = d.pop("file", UNSET)
        file: Union[Unset, File]
        if isinstance(_file, Unset):
            file = UNSET
        else:
            file = File(payload=BytesIO(_file))

        _plan = d.pop("plan", UNSET)
        plan: Union[Unset, ConvertAnnotationPlan]
        if isinstance(_plan, Unset):
            plan = UNSET
        else:
            plan = ConvertAnnotationPlan.from_dict(_plan)

        annotate_binary_form = cls(
            file=file,
            plan=plan,
        )

        return annotate_binary_form
