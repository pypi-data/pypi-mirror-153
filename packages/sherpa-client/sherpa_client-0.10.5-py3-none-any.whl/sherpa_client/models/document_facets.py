from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.metadata_count import MetadataCount

T = TypeVar("T", bound="DocumentFacets")


@attr.s(auto_attribs=True)
class DocumentFacets:
    """
    Attributes:
        facets (List[MetadataCount]):
        metadata (str):
    """

    facets: List[MetadataCount]
    metadata: str

    def to_dict(self) -> Dict[str, Any]:
        facets = []
        for facets_item_data in self.facets:
            facets_item = facets_item_data.to_dict()

            facets.append(facets_item)

        metadata = self.metadata

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "facets": facets,
                "metadata": metadata,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        facets = []
        _facets = d.pop("facets")
        for facets_item_data in _facets:
            facets_item = MetadataCount.from_dict(facets_item_data)

            facets.append(facets_item)

        metadata = d.pop("metadata")

        document_facets = cls(
            facets=facets,
            metadata=metadata,
        )

        return document_facets
