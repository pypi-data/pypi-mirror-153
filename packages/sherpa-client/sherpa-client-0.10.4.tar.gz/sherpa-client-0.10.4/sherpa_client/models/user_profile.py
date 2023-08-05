from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserProfile")


@attr.s(auto_attribs=True)
class UserProfile:
    """
    Attributes:
        profilename (str):
        username (str):
        email (Union[Unset, str]):
    """

    profilename: str
    username: str
    email: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        profilename = self.profilename
        username = self.username
        email = self.email

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "profilename": profilename,
                "username": username,
            }
        )
        if email is not UNSET:
            field_dict["email"] = email

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        profilename = d.pop("profilename")

        username = d.pop("username")

        email = d.pop("email", UNSET)

        user_profile = cls(
            profilename=profilename,
            username=username,
            email=email,
        )

        return user_profile
