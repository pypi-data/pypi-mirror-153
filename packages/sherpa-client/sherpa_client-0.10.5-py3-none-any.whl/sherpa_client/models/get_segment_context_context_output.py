from enum import Enum


class GetSegmentContextContextOutput(str, Enum):
    SEGMENTS = "segments"
    MERGED_SEGMENTS = "merged_segments"
    ALL = "all"

    def __str__(self) -> str:
        return str(self.value)
