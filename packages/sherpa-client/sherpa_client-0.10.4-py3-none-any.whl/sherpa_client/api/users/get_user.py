from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.user_response import UserResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    username: str,
    *,
    client: Client,
    admin_data: Union[Unset, None, bool] = True,
    jwt_format: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/users/{username}".format(client.base_url, username=username)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["adminData"] = admin_data

    params["jwtFormat"] = jwt_format

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, UserResponse]]:
    if response.status_code == 200:
        response_200 = UserResponse.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, UserResponse]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    username: str,
    *,
    client: Client,
    admin_data: Union[Unset, None, bool] = True,
    jwt_format: Union[Unset, None, bool] = False,
) -> Response[Union[Any, UserResponse]]:
    """Get user

    Args:
        username (str):
        admin_data (Union[Unset, None, bool]):  Default: True.
        jwt_format (Union[Unset, None, bool]):

    Returns:
        Response[Union[Any, UserResponse]]
    """

    kwargs = _get_kwargs(
        username=username,
        client=client,
        admin_data=admin_data,
        jwt_format=jwt_format,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    username: str,
    *,
    client: Client,
    admin_data: Union[Unset, None, bool] = True,
    jwt_format: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, UserResponse]]:
    """Get user

    Args:
        username (str):
        admin_data (Union[Unset, None, bool]):  Default: True.
        jwt_format (Union[Unset, None, bool]):

    Returns:
        Response[Union[Any, UserResponse]]
    """

    return sync_detailed(
        username=username,
        client=client,
        admin_data=admin_data,
        jwt_format=jwt_format,
    ).parsed


async def asyncio_detailed(
    username: str,
    *,
    client: Client,
    admin_data: Union[Unset, None, bool] = True,
    jwt_format: Union[Unset, None, bool] = False,
) -> Response[Union[Any, UserResponse]]:
    """Get user

    Args:
        username (str):
        admin_data (Union[Unset, None, bool]):  Default: True.
        jwt_format (Union[Unset, None, bool]):

    Returns:
        Response[Union[Any, UserResponse]]
    """

    kwargs = _get_kwargs(
        username=username,
        client=client,
        admin_data=admin_data,
        jwt_format=jwt_format,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    username: str,
    *,
    client: Client,
    admin_data: Union[Unset, None, bool] = True,
    jwt_format: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, UserResponse]]:
    """Get user

    Args:
        username (str):
        admin_data (Union[Unset, None, bool]):  Default: True.
        jwt_format (Union[Unset, None, bool]):

    Returns:
        Response[Union[Any, UserResponse]]
    """

    return (
        await asyncio_detailed(
            username=username,
            client=client,
            admin_data=admin_data,
            jwt_format=jwt_format,
        )
    ).parsed
