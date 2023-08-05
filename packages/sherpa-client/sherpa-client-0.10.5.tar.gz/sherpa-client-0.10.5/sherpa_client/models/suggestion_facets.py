from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.label_count import LabelCount
from ..models.text_count import TextCount

T = TypeVar("T", bound="SuggestionFacets")


@attr.s(auto_attribs=True)
class SuggestionFacets:
    """
    Attributes:
        labels (List[LabelCount]):
        texts (List[TextCount]):
    """

    labels: List[LabelCount]
    texts: List[TextCount]

    def to_dict(self) -> Dict[str, Any]:
        labels = []
        for labels_item_data in self.labels:
            labels_item = labels_item_data.to_dict()

            labels.append(labels_item)

        texts = []
        for texts_item_data in self.texts:
            texts_item = texts_item_data.to_dict()

            texts.append(texts_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "labels": labels,
                "texts": texts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        labels = []
        _labels = d.pop("labels")
        for labels_item_data in _labels:
            labels_item = LabelCount.from_dict(labels_item_data)

            labels.append(labels_item)

        texts = []
        _texts = d.pop("texts")
        for texts_item_data in _texts:
            texts_item = TextCount.from_dict(texts_item_data)

            texts.append(texts_item)

        suggestion_facets = cls(
            labels=labels,
            texts=texts,
        )

        return suggestion_facets
