from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="DocSentence")


@attr.s(auto_attribs=True)
class DocSentence:
    """
    Attributes:
        end (int):
        start (int):
    """

    end: int
    start: int

    def to_dict(self) -> Dict[str, Any]:
        end = self.end
        start = self.start

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "end": end,
                "start": start,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        end = d.pop("end")

        start = d.pop("start")

        doc_sentence = cls(
            end=end,
            start=start,
        )

        return doc_sentence
