from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.converter import Converter
from ..models.formatter import Formatter
from ..models.with_annotator import WithAnnotator
from ..models.with_processor import WithProcessor
from ..types import UNSET, Unset

T = TypeVar("T", bound="AnnotationPlan")


@attr.s(auto_attribs=True)
class AnnotationPlan:
    """
    Attributes:
        pipeline (List[Union[WithAnnotator, WithProcessor]]):
        converter (Union[Unset, Converter]):
        formatter (Union[Unset, Formatter]):
    """

    pipeline: List[Union[WithAnnotator, WithProcessor]]
    converter: Union[Unset, Converter] = UNSET
    formatter: Union[Unset, Formatter] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        pipeline = []
        for pipeline_item_data in self.pipeline:

            if isinstance(pipeline_item_data, WithAnnotator):
                pipeline_item = pipeline_item_data.to_dict()

            else:
                pipeline_item = pipeline_item_data.to_dict()

            pipeline.append(pipeline_item)

        converter: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.converter, Unset):
            converter = self.converter.to_dict()

        formatter: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.formatter, Unset):
            formatter = self.formatter.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "pipeline": pipeline,
            }
        )
        if converter is not UNSET:
            field_dict["converter"] = converter
        if formatter is not UNSET:
            field_dict["formatter"] = formatter

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        pipeline = []
        _pipeline = d.pop("pipeline")
        for pipeline_item_data in _pipeline:

            def _parse_pipeline_item(data: object) -> Union[WithAnnotator, WithProcessor]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    pipeline_item_type_0 = WithAnnotator.from_dict(data)

                    return pipeline_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                pipeline_item_type_1 = WithProcessor.from_dict(data)

                return pipeline_item_type_1

            pipeline_item = _parse_pipeline_item(pipeline_item_data)

            pipeline.append(pipeline_item)

        _converter = d.pop("converter", UNSET)
        converter: Union[Unset, Converter]
        if isinstance(_converter, Unset):
            converter = UNSET
        else:
            converter = Converter.from_dict(_converter)

        _formatter = d.pop("formatter", UNSET)
        formatter: Union[Unset, Formatter]
        if isinstance(_formatter, Unset):
            formatter = UNSET
        else:
            formatter = Formatter.from_dict(_formatter)

        annotation_plan = cls(
            pipeline=pipeline,
            converter=converter,
            formatter=formatter,
        )

        return annotation_plan
