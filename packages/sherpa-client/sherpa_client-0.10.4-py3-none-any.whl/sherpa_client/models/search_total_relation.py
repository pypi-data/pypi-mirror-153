from enum import Enum


class SearchTotalRelation(str, Enum):
    EQ = "eq"
    GTE = "gte"

    def __str__(self) -> str:
        return str(self.value)
