from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.user_profile import UserProfile
from ...types import UNSET, Response, Unset


def _get_kwargs(
    username: str,
    *,
    client: Client,
    private_data: Union[Unset, None, bool] = True,
) -> Dict[str, Any]:
    url = "{}/users/{username}/profile".format(client.base_url, username=username)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["privateData"] = private_data

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, UserProfile]]:
    if response.status_code == 200:
        response_200 = UserProfile.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, UserProfile]]:
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
    private_data: Union[Unset, None, bool] = True,
) -> Response[Union[Any, UserProfile]]:
    """Get user profile

    Args:
        username (str):
        private_data (Union[Unset, None, bool]):  Default: True.

    Returns:
        Response[Union[Any, UserProfile]]
    """

    kwargs = _get_kwargs(
        username=username,
        client=client,
        private_data=private_data,
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
    private_data: Union[Unset, None, bool] = True,
) -> Optional[Union[Any, UserProfile]]:
    """Get user profile

    Args:
        username (str):
        private_data (Union[Unset, None, bool]):  Default: True.

    Returns:
        Response[Union[Any, UserProfile]]
    """

    return sync_detailed(
        username=username,
        client=client,
        private_data=private_data,
    ).parsed


async def asyncio_detailed(
    username: str,
    *,
    client: Client,
    private_data: Union[Unset, None, bool] = True,
) -> Response[Union[Any, UserProfile]]:
    """Get user profile

    Args:
        username (str):
        private_data (Union[Unset, None, bool]):  Default: True.

    Returns:
        Response[Union[Any, UserProfile]]
    """

    kwargs = _get_kwargs(
        username=username,
        client=client,
        private_data=private_data,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    username: str,
    *,
    client: Client,
    private_data: Union[Unset, None, bool] = True,
) -> Optional[Union[Any, UserProfile]]:
    """Get user profile

    Args:
        username (str):
        private_data (Union[Unset, None, bool]):  Default: True.

    Returns:
        Response[Union[Any, UserProfile]]
    """

    return (
        await asyncio_detailed(
            username=username,
            client=client,
            private_data=private_data,
        )
    ).parsed
