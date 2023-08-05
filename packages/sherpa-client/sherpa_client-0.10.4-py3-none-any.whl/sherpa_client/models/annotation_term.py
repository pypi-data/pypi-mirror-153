from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.annotation_term_properties import AnnotationTermProperties
from ..types import UNSET, Unset

T = TypeVar("T", bound="AnnotationTerm")


@attr.s(auto_attribs=True)
class AnnotationTerm:
    """A term

    Attributes:
        identifier (str): Annotation identifier (only in 'html version')
        lexicon (str): Lexicon of the term
        preferred_form (Union[Unset, str]): Preferred form of the term
        properties (Union[Unset, AnnotationTermProperties]): Properties of the term
        score (Union[Unset, int]): Score of the term
    """

    identifier: str
    lexicon: str
    preferred_form: Union[Unset, str] = UNSET
    properties: Union[Unset, AnnotationTermProperties] = UNSET
    score: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        identifier = self.identifier
        lexicon = self.lexicon
        preferred_form = self.preferred_form
        properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        score = self.score

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "identifier": identifier,
                "lexicon": lexicon,
            }
        )
        if preferred_form is not UNSET:
            field_dict["preferredForm"] = preferred_form
        if properties is not UNSET:
            field_dict["properties"] = properties
        if score is not UNSET:
            field_dict["score"] = score

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        identifier = d.pop("identifier")

        lexicon = d.pop("lexicon")

        preferred_form = d.pop("preferredForm", UNSET)

        _properties = d.pop("properties", UNSET)
        properties: Union[Unset, AnnotationTermProperties]
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = AnnotationTermProperties.from_dict(_properties)

        score = d.pop("score", UNSET)

        annotation_term = cls(
            identifier=identifier,
            lexicon=lexicon,
            preferred_form=preferred_form,
            properties=properties,
            score=score,
        )

        return annotation_term
