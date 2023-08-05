from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.formatter import Formatter
from ..models.with_annotator import WithAnnotator
from ..models.with_processor import WithProcessor

T = TypeVar("T", bound="FormatTextWithMany")


@attr.s(auto_attribs=True)
class FormatTextWithMany:
    """
    Attributes:
        formatter (Formatter):
        pipeline (List[Union[WithAnnotator, WithProcessor]]):
        text (str):
    """

    formatter: Formatter
    pipeline: List[Union[WithAnnotator, WithProcessor]]
    text: str

    def to_dict(self) -> Dict[str, Any]:
        formatter = self.formatter.to_dict()

        pipeline = []
        for pipeline_item_data in self.pipeline:

            if isinstance(pipeline_item_data, WithAnnotator):
                pipeline_item = pipeline_item_data.to_dict()

            else:
                pipeline_item = pipeline_item_data.to_dict()

            pipeline.append(pipeline_item)

        text = self.text

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "formatter": formatter,
                "pipeline": pipeline,
                "text": text,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        formatter = Formatter.from_dict(d.pop("formatter"))

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

        text = d.pop("text")

        format_text_with_many = cls(
            formatter=formatter,
            pipeline=pipeline,
            text=text,
        )

        return format_text_with_many
