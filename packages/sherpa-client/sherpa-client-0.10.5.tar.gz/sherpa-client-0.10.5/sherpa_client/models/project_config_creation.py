from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.project_config_creation_properties import ProjectConfigCreationProperties
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectConfigCreation")


@attr.s(auto_attribs=True)
class ProjectConfigCreation:
    """
    Attributes:
        description (Union[Unset, str]):
        image_filename (Union[Unset, str]):
        image_id (Union[Unset, str]):
        image_url (Union[Unset, str]):
        label (Union[Unset, str]):
        lang (Union[Unset, str]):  Default: 'en'.
        metafacets (Union[Unset, str]):
        name (Union[Unset, str]):
        nature (Union[Unset, str]):  Default: 'sequence_labelling'.
        properties (Union[Unset, ProjectConfigCreationProperties]):
    """

    description: Union[Unset, str] = UNSET
    image_filename: Union[Unset, str] = UNSET
    image_id: Union[Unset, str] = UNSET
    image_url: Union[Unset, str] = UNSET
    label: Union[Unset, str] = UNSET
    lang: Union[Unset, str] = "en"
    metafacets: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    nature: Union[Unset, str] = "sequence_labelling"
    properties: Union[Unset, ProjectConfigCreationProperties] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        description = self.description
        image_filename = self.image_filename
        image_id = self.image_id
        image_url = self.image_url
        label = self.label
        lang = self.lang
        metafacets = self.metafacets
        name = self.name
        nature = self.nature
        properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if image_filename is not UNSET:
            field_dict["imageFilename"] = image_filename
        if image_id is not UNSET:
            field_dict["imageId"] = image_id
        if image_url is not UNSET:
            field_dict["imageUrl"] = image_url
        if label is not UNSET:
            field_dict["label"] = label
        if lang is not UNSET:
            field_dict["lang"] = lang
        if metafacets is not UNSET:
            field_dict["metafacets"] = metafacets
        if name is not UNSET:
            field_dict["name"] = name
        if nature is not UNSET:
            field_dict["nature"] = nature
        if properties is not UNSET:
            field_dict["properties"] = properties

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        description = d.pop("description", UNSET)

        image_filename = d.pop("imageFilename", UNSET)

        image_id = d.pop("imageId", UNSET)

        image_url = d.pop("imageUrl", UNSET)

        label = d.pop("label", UNSET)

        lang = d.pop("lang", UNSET)

        metafacets = d.pop("metafacets", UNSET)

        name = d.pop("name", UNSET)

        nature = d.pop("nature", UNSET)

        _properties = d.pop("properties", UNSET)
        properties: Union[Unset, ProjectConfigCreationProperties]
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = ProjectConfigCreationProperties.from_dict(_properties)

        project_config_creation = cls(
            description=description,
            image_filename=image_filename,
            image_id=image_id,
            image_url=image_url,
            label=label,
            lang=lang,
            metafacets=metafacets,
            name=name,
            nature=nature,
            properties=properties,
        )

        return project_config_creation
