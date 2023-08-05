from enum import Enum


class RequestJwtTokenProjectAccessMode(str, Enum):
    READ = "read"
    WRITE = "write"
    CHMOD = "chmod"

    def __str__(self) -> str:
        return str(self.value)
