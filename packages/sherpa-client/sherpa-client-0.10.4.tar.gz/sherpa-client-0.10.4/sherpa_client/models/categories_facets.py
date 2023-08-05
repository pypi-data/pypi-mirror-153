from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.label_count import LabelCount

T = TypeVar("T", bound="CategoriesFacets")


@attr.s(auto_attribs=True)
class CategoriesFacets:
    """
    Attributes:
        labels (List[LabelCount]):
    """

    labels: List[LabelCount]

    def to_dict(self) -> Dict[str, Any]:
        labels = []
        for labels_item_data in self.labels:
            labels_item = labels_item_data.to_dict()

            labels.append(labels_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "labels": labels,
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

        categories_facets = cls(
            labels=labels,
        )

        return categories_facets
