from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserResponse")


@attr.s(auto_attribs=True)
class UserResponse:
    """
    Attributes:
        profilename (str):
        username (str):
        created_at (Union[Unset, str]):
        created_by (Union[Unset, str]):
        default_group (Union[Unset, str]):
        email (Union[Unset, str]):
        groups (Union[Unset, List[str]]):
        permissions (Union[Unset, List[str]]):
        roles (Union[Unset, List[str]]):
    """

    profilename: str
    username: str
    created_at: Union[Unset, str] = UNSET
    created_by: Union[Unset, str] = UNSET
    default_group: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    groups: Union[Unset, List[str]] = UNSET
    permissions: Union[Unset, List[str]] = UNSET
    roles: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        profilename = self.profilename
        username = self.username
        created_at = self.created_at
        created_by = self.created_by
        default_group = self.default_group
        email = self.email
        groups: Union[Unset, List[str]] = UNSET
        if not isinstance(self.groups, Unset):
            groups = self.groups

        permissions: Union[Unset, List[str]] = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = self.permissions

        roles: Union[Unset, List[str]] = UNSET
        if not isinstance(self.roles, Unset):
            roles = self.roles

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "profilename": profilename,
                "username": username,
            }
        )
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if default_group is not UNSET:
            field_dict["defaultGroup"] = default_group
        if email is not UNSET:
            field_dict["email"] = email
        if groups is not UNSET:
            field_dict["groups"] = groups
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if roles is not UNSET:
            field_dict["roles"] = roles

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        profilename = d.pop("profilename")

        username = d.pop("username")

        created_at = d.pop("createdAt", UNSET)

        created_by = d.pop("createdBy", UNSET)

        default_group = d.pop("defaultGroup", UNSET)

        email = d.pop("email", UNSET)

        groups = cast(List[str], d.pop("groups", UNSET))

        permissions = cast(List[str], d.pop("permissions", UNSET))

        roles = cast(List[str], d.pop("roles", UNSET))

        user_response = cls(
            profilename=profilename,
            username=username,
            created_at=created_at,
            created_by=created_by,
            default_group=default_group,
            email=email,
            groups=groups,
            permissions=permissions,
            roles=roles,
        )

        return user_response
