from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.http_service_metadata_operations import HttpServiceMetadataOperations
from ..types import UNSET, Unset

T = TypeVar("T", bound="HttpServiceMetadata")


@attr.s(auto_attribs=True)
class HttpServiceMetadata:
    """
    Attributes:
        api (str):
        compatibility (str):
        version (str):
        annotators (Union[Unset, str]):
        converters (Union[Unset, str]):
        engine (Union[Unset, str]):
        extensions (Union[Unset, str]):
        formatters (Union[Unset, str]):
        functions (Union[Unset, str]):
        languages (Union[Unset, str]):
        natures (Union[Unset, str]):
        operations (Union[Unset, HttpServiceMetadataOperations]):
        processors (Union[Unset, str]):
        term_importers (Union[Unset, str]):
        trigger (Union[Unset, str]):
    """

    api: str
    compatibility: str
    version: str
    annotators: Union[Unset, str] = UNSET
    converters: Union[Unset, str] = UNSET
    engine: Union[Unset, str] = UNSET
    extensions: Union[Unset, str] = UNSET
    formatters: Union[Unset, str] = UNSET
    functions: Union[Unset, str] = UNSET
    languages: Union[Unset, str] = UNSET
    natures: Union[Unset, str] = UNSET
    operations: Union[Unset, HttpServiceMetadataOperations] = UNSET
    processors: Union[Unset, str] = UNSET
    term_importers: Union[Unset, str] = UNSET
    trigger: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        api = self.api
        compatibility = self.compatibility
        version = self.version
        annotators = self.annotators
        converters = self.converters
        engine = self.engine
        extensions = self.extensions
        formatters = self.formatters
        functions = self.functions
        languages = self.languages
        natures = self.natures
        operations: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.operations, Unset):
            operations = self.operations.to_dict()

        processors = self.processors
        term_importers = self.term_importers
        trigger = self.trigger

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "api": api,
                "compatibility": compatibility,
                "version": version,
            }
        )
        if annotators is not UNSET:
            field_dict["annotators"] = annotators
        if converters is not UNSET:
            field_dict["converters"] = converters
        if engine is not UNSET:
            field_dict["engine"] = engine
        if extensions is not UNSET:
            field_dict["extensions"] = extensions
        if formatters is not UNSET:
            field_dict["formatters"] = formatters
        if functions is not UNSET:
            field_dict["functions"] = functions
        if languages is not UNSET:
            field_dict["languages"] = languages
        if natures is not UNSET:
            field_dict["natures"] = natures
        if operations is not UNSET:
            field_dict["operations"] = operations
        if processors is not UNSET:
            field_dict["processors"] = processors
        if term_importers is not UNSET:
            field_dict["termImporters"] = term_importers
        if trigger is not UNSET:
            field_dict["trigger"] = trigger

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        api = d.pop("api")

        compatibility = d.pop("compatibility")

        version = d.pop("version")

        annotators = d.pop("annotators", UNSET)

        converters = d.pop("converters", UNSET)

        engine = d.pop("engine", UNSET)

        extensions = d.pop("extensions", UNSET)

        formatters = d.pop("formatters", UNSET)

        functions = d.pop("functions", UNSET)

        languages = d.pop("languages", UNSET)

        natures = d.pop("natures", UNSET)

        _operations = d.pop("operations", UNSET)
        operations: Union[Unset, HttpServiceMetadataOperations]
        if isinstance(_operations, Unset):
            operations = UNSET
        else:
            operations = HttpServiceMetadataOperations.from_dict(_operations)

        processors = d.pop("processors", UNSET)

        term_importers = d.pop("termImporters", UNSET)

        trigger = d.pop("trigger", UNSET)

        http_service_metadata = cls(
            api=api,
            compatibility=compatibility,
            version=version,
            annotators=annotators,
            converters=converters,
            engine=engine,
            extensions=extensions,
            formatters=formatters,
            functions=functions,
            languages=languages,
            natures=natures,
            operations=operations,
            processors=processors,
            term_importers=term_importers,
            trigger=trigger,
        )

        return http_service_metadata
