from enum import Enum


class DocAnnotationStatus(str, Enum):
    OK = "OK"
    KO = "KO"

    def __str__(self) -> str:
        return str(self.value)
