from enum import Enum


class CategoryStatus(str, Enum):
    OK = "OK"
    KO = "KO"

    def __str__(self) -> str:
        return str(self.value)
