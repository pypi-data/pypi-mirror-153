from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="OperationCount")


@attr.s(auto_attribs=True)
class OperationCount:
    """Annotation creation response

    Attributes:
        count (int): Number of elements affected by the operation
        operation (str): Name of the operation
        unit (str): Element unit of the operation
    """

    count: int
    operation: str
    unit: str

    def to_dict(self) -> Dict[str, Any]:
        count = self.count
        operation = self.operation
        unit = self.unit

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "count": count,
                "operation": operation,
                "unit": unit,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        count = d.pop("count")

        operation = d.pop("operation")

        unit = d.pop("unit")

        operation_count = cls(
            count=count,
            operation=operation,
            unit=unit,
        )

        return operation_count
