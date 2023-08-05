from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.classification_config import ClassificationConfig
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectBean")


@attr.s(auto_attribs=True)
class ProjectBean:
    """
    Attributes:
        description (str):
        image (str):
        label (str):
        lang (str):
        name (str):
        algorithms (Union[Unset, List[str]]):
        annotations (Union[Unset, int]):
        categories (Union[Unset, int]):
        classification (Union[Unset, ClassificationConfig]):
        created_by (Union[Unset, str]):
        created_date (Union[Unset, str]):
        documents (Union[Unset, int]):
        engines (Union[Unset, List[str]]):
        group_name (Union[Unset, str]):
        metafacets (Union[Unset, List[Any]]):
        nature (Union[Unset, str]):
        owner (Union[Unset, str]):
        private (Union[Unset, bool]):
        read_only (Union[Unset, bool]):
        segments (Union[Unset, int]):
        shared (Union[Unset, bool]):
        version (Union[Unset, str]):
    """

    image: str
    label: str
    lang: str
    name: str
    algorithms: Union[Unset, List[str]] = UNSET
    annotations: Union[Unset, int] = UNSET
    categories: Union[Unset, int] = UNSET
    classification: Union[Unset, ClassificationConfig] = UNSET
    description: Union[Unset, str] = UNSET
    created_by: Union[Unset, str] = UNSET
    created_date: Union[Unset, str] = UNSET
    documents: Union[Unset, int] = UNSET
    engines: Union[Unset, List[str]] = UNSET
    group_name: Union[Unset, str] = UNSET
    metafacets: Union[Unset, List[Any]] = UNSET
    nature: Union[Unset, str] = UNSET
    owner: Union[Unset, str] = UNSET
    private: Union[Unset, bool] = UNSET
    read_only: Union[Unset, bool] = UNSET
    segments: Union[Unset, int] = UNSET
    shared: Union[Unset, bool] = UNSET
    version: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        image = self.image
        label = self.label
        lang = self.lang
        name = self.name
        algorithms: Union[Unset, List[str]] = UNSET
        if not isinstance(self.algorithms, Unset):
            algorithms = self.algorithms

        annotations = self.annotations
        categories = self.categories
        classification: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.classification, Unset):
            classification = self.classification.to_dict()

        description = self.description
        created_by = self.created_by
        created_date = self.created_date
        documents = self.documents
        engines: Union[Unset, List[str]] = UNSET
        if not isinstance(self.engines, Unset):
            engines = self.engines

        group_name = self.group_name
        metafacets: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.metafacets, Unset):
            metafacets = []
            for metafacets_item_data in self.metafacets:
                metafacets_item = metafacets_item_data

                metafacets.append(metafacets_item)

        nature = self.nature
        owner = self.owner
        private = self.private
        read_only = self.read_only
        segments = self.segments
        shared = self.shared
        version = self.version

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "description": description,
                "image": image,
                "label": label,
                "lang": lang,
                "name": name,
            }
        )
        if algorithms is not UNSET:
            field_dict["algorithms"] = algorithms
        if annotations is not UNSET:
            field_dict["annotations"] = annotations
        if categories is not UNSET:
            field_dict["categories"] = categories
        if classification is not UNSET:
            field_dict["classification"] = classification
        if description is not UNSET:
            field_dict["description"] = description
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if created_date is not UNSET:
            field_dict["createdDate"] = created_date
        if documents is not UNSET:
            field_dict["documents"] = documents
        if engines is not UNSET:
            field_dict["engines"] = engines
        if group_name is not UNSET:
            field_dict["groupName"] = group_name
        if metafacets is not UNSET:
            field_dict["metafacets"] = metafacets
        if nature is not UNSET:
            field_dict["nature"] = nature
        if owner is not UNSET:
            field_dict["owner"] = owner
        if private is not UNSET:
            field_dict["private"] = private
        if read_only is not UNSET:
            field_dict["readOnly"] = read_only
        if segments is not UNSET:
            field_dict["segments"] = segments
        if shared is not UNSET:
            field_dict["shared"] = shared
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        image = d.pop("image")

        label = d.pop("label")

        lang = d.pop("lang")

        name = d.pop("name")

        algorithms = cast(List[str], d.pop("algorithms", UNSET))

        annotations = d.pop("annotations", UNSET)

        categories = d.pop("categories", UNSET)

        _classification = d.pop("classification", UNSET)
        classification: Union[Unset, ClassificationConfig]
        if isinstance(_classification, Unset):
            classification = UNSET
        else:
            classification = ClassificationConfig.from_dict(_classification)

        description = d.pop("description", UNSET)

        created_by = d.pop("createdBy", UNSET)

        created_date = d.pop("createdDate", UNSET)

        documents = d.pop("documents", UNSET)

        engines = cast(List[str], d.pop("engines", UNSET))

        group_name = d.pop("groupName", UNSET)

        metafacets = []
        _metafacets = d.pop("metafacets", UNSET)
        for metafacets_item_data in _metafacets or []:
            metafacets_item = metafacets_item_data

            metafacets.append(metafacets_item)

        nature = d.pop("nature", UNSET)

        owner = d.pop("owner", UNSET)

        private = d.pop("private", UNSET)

        read_only = d.pop("readOnly", UNSET)

        segments = d.pop("segments", UNSET)

        shared = d.pop("shared", UNSET)

        version = d.pop("version", UNSET)

        project_bean = cls(
            description=description,
            image=image,
            label=label,
            lang=lang,
            name=name,
            algorithms=algorithms,
            annotations=annotations,
            categories=categories,
            classification=classification,
            created_by=created_by,
            created_date=created_date,
            documents=documents,
            engines=engines,
            group_name=group_name,
            metafacets=metafacets,
            nature=nature,
            owner=owner,
            private=private,
            read_only=read_only,
            segments=segments,
            shared=shared,
            version=version,
        )

        return project_bean
