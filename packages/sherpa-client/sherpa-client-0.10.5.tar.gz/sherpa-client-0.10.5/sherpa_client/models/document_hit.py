from typing import Any, Dict, Type, TypeVar

import attr

from ..models.document import Document

T = TypeVar("T", bound="DocumentHit")


@attr.s(auto_attribs=True)
class DocumentHit:
    """
    Attributes:
        id (str):
        document (Document):
        score (float):
    """

    id: str
    document: Document
    score: float

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        document = self.document.to_dict()

        score = self.score

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "_id": id,
                "document": document,
                "score": score,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("_id")

        document = Document.from_dict(d.pop("document"))

        score = d.pop("score")

        document_hit = cls(
            id=id,
            document=document,
            score=score,
        )

        return document_hit
