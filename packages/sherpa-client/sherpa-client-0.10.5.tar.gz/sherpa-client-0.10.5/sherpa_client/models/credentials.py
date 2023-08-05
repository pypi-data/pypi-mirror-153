from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="Credentials")


@attr.s(auto_attribs=True)
class Credentials:
    """
    Attributes:
        email (str):
        password (str):
    """

    email: str
    password: str

    def to_dict(self) -> Dict[str, Any]:
        email = self.email
        password = self.password

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "email": email,
                "password": password,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        email = d.pop("email")

        password = d.pop("password")

        credentials = cls(
            email=email,
            password=password,
        )

        return credentials
