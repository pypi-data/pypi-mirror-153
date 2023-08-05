from typing import Any, Dict, Type, TypeVar

import attr

from ..models.share_mode import ShareMode

T = TypeVar("T", bound="GroupShare")


@attr.s(auto_attribs=True)
class GroupShare:
    """
    Attributes:
        can_revoke (bool):
        group_name (str):
        mode (ShareMode):
    """

    can_revoke: bool
    group_name: str
    mode: ShareMode

    def to_dict(self) -> Dict[str, Any]:
        can_revoke = self.can_revoke
        group_name = self.group_name
        mode = self.mode.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "canRevoke": can_revoke,
                "groupName": group_name,
                "mode": mode,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        can_revoke = d.pop("canRevoke")

        group_name = d.pop("groupName")

        mode = ShareMode.from_dict(d.pop("mode"))

        group_share = cls(
            can_revoke=can_revoke,
            group_name=group_name,
            mode=mode,
        )

        return group_share
