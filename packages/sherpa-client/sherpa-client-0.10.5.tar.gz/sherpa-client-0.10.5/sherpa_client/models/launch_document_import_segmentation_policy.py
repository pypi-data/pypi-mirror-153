from enum import Enum


class LaunchDocumentImportSegmentationPolicy(str, Enum):
    ALWAYS_RECOMPUTE = "always_recompute"
    COMPUTE_IF_MISSING = "compute_if_missing"
    NO_SEGMENTATION = "no_segmentation"
    DOCUMENTS_AS_SEGMENTS = "documents_as_segments"

    def __str__(self) -> str:
        return str(self.value)
