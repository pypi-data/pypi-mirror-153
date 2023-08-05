from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="MetadataDefinitionEntry")


@attr.s(auto_attribs=True)
class MetadataDefinitionEntry:
    """
    Attributes:
        distinct_metadata_values (List[str]):
        is_editable (bool):
        is_multiple (bool):
        metadata_name (str):
    """

    distinct_metadata_values: List[str]
    is_editable: bool
    is_multiple: bool
    metadata_name: str

    def to_dict(self) -> Dict[str, Any]:
        distinct_metadata_values = self.distinct_metadata_values

        is_editable = self.is_editable
        is_multiple = self.is_multiple
        metadata_name = self.metadata_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "distinctMetadataValues": distinct_metadata_values,
                "isEditable": is_editable,
                "isMultiple": is_multiple,
                "metadataName": metadata_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        distinct_metadata_values = cast(List[str], d.pop("distinctMetadataValues"))

        is_editable = d.pop("isEditable")

        is_multiple = d.pop("isMultiple")

        metadata_name = d.pop("metadataName")

        metadata_definition_entry = cls(
            distinct_metadata_values=distinct_metadata_values,
            is_editable=is_editable,
            is_multiple=is_multiple,
            metadata_name=metadata_name,
        )

        return metadata_definition_entry
