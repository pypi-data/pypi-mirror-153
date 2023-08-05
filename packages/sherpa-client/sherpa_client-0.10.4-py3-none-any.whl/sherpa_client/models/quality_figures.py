from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="QualityFigures")


@attr.s(auto_attribs=True)
class QualityFigures:
    """
    Attributes:
        f1 (float):
        precision (float):
        recall (float):
        support (int):
        roc_auc (Union[Unset, float]):
    """

    f1: float
    precision: float
    recall: float
    support: int
    roc_auc: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        f1 = self.f1
        precision = self.precision
        recall = self.recall
        support = self.support
        roc_auc = self.roc_auc

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "f1": f1,
                "precision": precision,
                "recall": recall,
                "support": support,
            }
        )
        if roc_auc is not UNSET:
            field_dict["roc_auc"] = roc_auc

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        f1 = d.pop("f1")

        precision = d.pop("precision")

        recall = d.pop("recall")

        support = d.pop("support")

        roc_auc = d.pop("roc_auc", UNSET)

        quality_figures = cls(
            f1=f1,
            precision=precision,
            recall=recall,
            support=support,
            roc_auc=roc_auc,
        )

        return quality_figures
