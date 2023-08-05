from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.annotated_doc_annotation_properties import AnnotatedDocAnnotationProperties
from ..models.annotation_term import AnnotationTerm
from ..types import UNSET, Unset

T = TypeVar("T", bound="AnnotatedDocAnnotation")


@attr.s(auto_attribs=True)
class AnnotatedDocAnnotation:
    """A document annotation

    Attributes:
        end (int): End offset in document
        label_name (str): Label name
        start (int): Start offset in document
        text (str): Covered text
        label (Union[Unset, str]): Human-friendly label
        label_id (Union[Unset, str]): External label identifier
        properties (Union[Unset, AnnotatedDocAnnotationProperties]): Additional properties
        score (Union[Unset, float]): Score of the annotation
        terms (Union[Unset, List[AnnotationTerm]]):
    """

    end: int
    label_name: str
    start: int
    text: str
    label: Union[Unset, str] = UNSET
    label_id: Union[Unset, str] = UNSET
    properties: Union[Unset, AnnotatedDocAnnotationProperties] = UNSET
    score: Union[Unset, float] = UNSET
    terms: Union[Unset, List[AnnotationTerm]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        end = self.end
        label_name = self.label_name
        start = self.start
        text = self.text
        label = self.label
        label_id = self.label_id
        properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        score = self.score
        terms: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.terms, Unset):
            terms = []
            for terms_item_data in self.terms:
                terms_item = terms_item_data.to_dict()

                terms.append(terms_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "end": end,
                "labelName": label_name,
                "start": start,
                "text": text,
            }
        )
        if label is not UNSET:
            field_dict["label"] = label
        if label_id is not UNSET:
            field_dict["labelId"] = label_id
        if properties is not UNSET:
            field_dict["properties"] = properties
        if score is not UNSET:
            field_dict["score"] = score
        if terms is not UNSET:
            field_dict["terms"] = terms

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        end = d.pop("end")

        label_name = d.pop("labelName")

        start = d.pop("start")

        text = d.pop("text")

        label = d.pop("label", UNSET)

        label_id = d.pop("labelId", UNSET)

        _properties = d.pop("properties", UNSET)
        properties: Union[Unset, AnnotatedDocAnnotationProperties]
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = AnnotatedDocAnnotationProperties.from_dict(_properties)

        score = d.pop("score", UNSET)

        terms = []
        _terms = d.pop("terms", UNSET)
        for terms_item_data in _terms or []:
            terms_item = AnnotationTerm.from_dict(terms_item_data)

            terms.append(terms_item)

        annotated_doc_annotation = cls(
            end=end,
            label_name=label_name,
            start=start,
            text=text,
            label=label,
            label_id=label_id,
            properties=properties,
            score=score,
            terms=terms,
        )

        return annotated_doc_annotation
