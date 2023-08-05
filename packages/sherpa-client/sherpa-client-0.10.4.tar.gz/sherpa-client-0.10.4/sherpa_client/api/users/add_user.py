from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.new_user import NewUser
from ...models.user_response import UserResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    json_body: NewUser,
    group_name: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/users".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["groupName"] = group_name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[UserResponse]:
    if response.status_code == 200:
        response_200 = UserResponse.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[UserResponse]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: NewUser,
    group_name: Union[Unset, None, str] = UNSET,
) -> Response[UserResponse]:
    """Add user

    Args:
        group_name (Union[Unset, None, str]):
        json_body (NewUser):

    Returns:
        Response[UserResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        group_name=group_name,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    json_body: NewUser,
    group_name: Union[Unset, None, str] = UNSET,
) -> Optional[UserResponse]:
    """Add user

    Args:
        group_name (Union[Unset, None, str]):
        json_body (NewUser):

    Returns:
        Response[UserResponse]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        group_name=group_name,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: NewUser,
    group_name: Union[Unset, None, str] = UNSET,
) -> Response[UserResponse]:
    """Add user

    Args:
        group_name (Union[Unset, None, str]):
        json_body (NewUser):

    Returns:
        Response[UserResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        group_name=group_name,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    json_body: NewUser,
    group_name: Union[Unset, None, str] = UNSET,
) -> Optional[UserResponse]:
    """Add user

    Args:
        group_name (Union[Unset, None, str]):
        json_body (NewUser):

    Returns:
        Response[UserResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            group_name=group_name,
        )
    ).parsed
