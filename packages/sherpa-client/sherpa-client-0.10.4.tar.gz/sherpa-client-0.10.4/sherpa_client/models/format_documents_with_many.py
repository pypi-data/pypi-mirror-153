from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.formatter import Formatter
from ..models.input_document import InputDocument
from ..models.with_annotator import WithAnnotator
from ..models.with_processor import WithProcessor

T = TypeVar("T", bound="FormatDocumentsWithMany")


@attr.s(auto_attribs=True)
class FormatDocumentsWithMany:
    """
    Attributes:
        documents (List[InputDocument]):
        formatter (Formatter):
        pipeline (List[Union[WithAnnotator, WithProcessor]]):
    """

    documents: List[InputDocument]
    formatter: Formatter
    pipeline: List[Union[WithAnnotator, WithProcessor]]

    def to_dict(self) -> Dict[str, Any]:
        documents = []
        for documents_item_data in self.documents:
            documents_item = documents_item_data.to_dict()

            documents.append(documents_item)

        formatter = self.formatter.to_dict()

        pipeline = []
        for pipeline_item_data in self.pipeline:

            if isinstance(pipeline_item_data, WithAnnotator):
                pipeline_item = pipeline_item_data.to_dict()

            else:
                pipeline_item = pipeline_item_data.to_dict()

            pipeline.append(pipeline_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "documents": documents,
                "formatter": formatter,
                "pipeline": pipeline,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        documents = []
        _documents = d.pop("documents")
        for documents_item_data in _documents:
            documents_item = InputDocument.from_dict(documents_item_data)

            documents.append(documents_item)

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

        format_documents_with_many = cls(
            documents=documents,
            formatter=formatter,
            pipeline=pipeline,
        )

        return format_documents_with_many
