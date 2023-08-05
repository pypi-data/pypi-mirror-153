from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.metadata_definition_entry import MetadataDefinitionEntry

T = TypeVar("T", bound="MetadataDefinition")


@attr.s(auto_attribs=True)
class MetadataDefinition:
    """
    Attributes:
        metadata (List[MetadataDefinitionEntry]):
    """

    metadata: List[MetadataDefinitionEntry]

    def to_dict(self) -> Dict[str, Any]:
        metadata = []
        for metadata_item_data in self.metadata:
            metadata_item = metadata_item_data.to_dict()

            metadata.append(metadata_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "metadata": metadata,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        metadata = []
        _metadata = d.pop("metadata")
        for metadata_item_data in _metadata:
            metadata_item = MetadataDefinitionEntry.from_dict(metadata_item_data)

            metadata.append(metadata_item)

        metadata_definition = cls(
            metadata=metadata,
        )

        return metadata_definition
