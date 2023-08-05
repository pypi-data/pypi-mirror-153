from typing import Any, Dict, Type, TypeVar

import attr

from ..models.categories_facets import CategoriesFacets
from ..models.document_facets import DocumentFacets

T = TypeVar("T", bound="CategoryMetrics")


@attr.s(auto_attribs=True)
class CategoryMetrics:
    """
    Attributes:
        categories_count (int):
        categories_facets (CategoriesFacets):
        document_facets (DocumentFacets):
        documents_in_dataset (int):
    """

    categories_count: int
    categories_facets: CategoriesFacets
    document_facets: DocumentFacets
    documents_in_dataset: int

    def to_dict(self) -> Dict[str, Any]:
        categories_count = self.categories_count
        categories_facets = self.categories_facets.to_dict()

        document_facets = self.document_facets.to_dict()

        documents_in_dataset = self.documents_in_dataset

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "categoriesCount": categories_count,
                "categoriesFacets": categories_facets,
                "documentFacets": document_facets,
                "documentsInDataset": documents_in_dataset,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        categories_count = d.pop("categoriesCount")

        categories_facets = CategoriesFacets.from_dict(d.pop("categoriesFacets"))

        document_facets = DocumentFacets.from_dict(d.pop("documentFacets"))

        documents_in_dataset = d.pop("documentsInDataset")

        category_metrics = cls(
            categories_count=categories_count,
            categories_facets=categories_facets,
            document_facets=document_facets,
            documents_in_dataset=documents_in_dataset,
        )

        return category_metrics
