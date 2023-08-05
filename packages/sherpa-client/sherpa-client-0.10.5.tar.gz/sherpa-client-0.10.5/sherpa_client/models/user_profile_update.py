from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserProfileUpdate")


@attr.s(auto_attribs=True)
class UserProfileUpdate:
    """
    Attributes:
        email (Union[Unset, str]):
        password (Union[Unset, str]):
        profilename (Union[Unset, str]):
    """

    email: Union[Unset, str] = UNSET
    password: Union[Unset, str] = UNSET
    profilename: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        email = self.email
        password = self.password
        profilename = self.profilename

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if email is not UNSET:
            field_dict["email"] = email
        if password is not UNSET:
            field_dict["password"] = password
        if profilename is not UNSET:
            field_dict["profilename"] = profilename

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        email = d.pop("email", UNSET)

        password = d.pop("password", UNSET)

        profilename = d.pop("profilename", UNSET)

        user_profile_update = cls(
            email=email,
            password=password,
            profilename=profilename,
        )

        return user_profile_update
