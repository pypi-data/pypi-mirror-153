from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.term_importer_spec import TermImporterSpec
from ..models.uploaded_file import UploadedFile

T = TypeVar("T", bound="TermImport")


@attr.s(auto_attribs=True)
class TermImport:
    """
    Attributes:
        files (List[UploadedFile]):
        importer (TermImporterSpec):
    """

    files: List[UploadedFile]
    importer: TermImporterSpec

    def to_dict(self) -> Dict[str, Any]:
        files = []
        for files_item_data in self.files:
            files_item = files_item_data.to_dict()

            files.append(files_item)

        importer = self.importer.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "files": files,
                "importer": importer,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        files = []
        _files = d.pop("files")
        for files_item_data in _files:
            files_item = UploadedFile.from_dict(files_item_data)

            files.append(files_item)

        importer = TermImporterSpec.from_dict(d.pop("importer"))

        term_import = cls(
            files=files,
            importer=importer,
        )

        return term_import
