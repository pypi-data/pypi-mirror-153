from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="DeleteGroupResult")


@attr.s(auto_attribs=True)
class DeleteGroupResult:
    """
    Attributes:
        removed_projects (int):
        removed_users (int):
    """

    removed_projects: int
    removed_users: int

    def to_dict(self) -> Dict[str, Any]:
        removed_projects = self.removed_projects
        removed_users = self.removed_users

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "removedProjects": removed_projects,
                "removedUsers": removed_users,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        removed_projects = d.pop("removedProjects")

        removed_users = d.pop("removedUsers")

        delete_group_result = cls(
            removed_projects=removed_projects,
            removed_users=removed_users,
        )

        return delete_group_result
