from typing import Any, Dict, Type, TypeVar

import attr

from ..models.term_importer_spec_parameters import TermImporterSpecParameters

T = TypeVar("T", bound="TermImporterSpec")


@attr.s(auto_attribs=True)
class TermImporterSpec:
    """
    Attributes:
        format_ (str):
        parameters (TermImporterSpecParameters):
    """

    format_: str
    parameters: TermImporterSpecParameters

    def to_dict(self) -> Dict[str, Any]:
        format_ = self.format_
        parameters = self.parameters.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "format": format_,
                "parameters": parameters,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        format_ = d.pop("format")

        parameters = TermImporterSpecParameters.from_dict(d.pop("parameters"))

        term_importer_spec = cls(
            format_=format_,
            parameters=parameters,
        )

        return term_importer_spec
