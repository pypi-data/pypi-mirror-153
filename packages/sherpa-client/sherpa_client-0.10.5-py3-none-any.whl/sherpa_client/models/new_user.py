from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="NewUser")


@attr.s(auto_attribs=True)
class NewUser:
    """
    Attributes:
        password (str):
        permissions (List[str]):
        roles (List[str]):
        username (str):
        email (Union[Unset, str]):
    """

    password: str
    permissions: List[str]
    roles: List[str]
    username: str
    email: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        password = self.password
        permissions = self.permissions

        roles = self.roles

        username = self.username
        email = self.email

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "password": password,
                "permissions": permissions,
                "roles": roles,
                "username": username,
            }
        )
        if email is not UNSET:
            field_dict["email"] = email

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        password = d.pop("password")

        permissions = cast(List[str], d.pop("permissions"))

        roles = cast(List[str], d.pop("roles"))

        username = d.pop("username")

        email = d.pop("email", UNSET)

        new_user = cls(
            password=password,
            permissions=permissions,
            roles=roles,
            username=username,
            email=email,
        )

        return new_user
