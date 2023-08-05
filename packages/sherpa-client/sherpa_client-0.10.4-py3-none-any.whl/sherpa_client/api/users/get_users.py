from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.user_response import UserResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    group_name: Union[Unset, None, str] = UNSET,
    admin_data: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/users".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["groupName"] = group_name

    params["adminData"] = admin_data

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[List[UserResponse]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_user_response_array_item_data in _response_200:
            componentsschemas_user_response_array_item = UserResponse.from_dict(
                componentsschemas_user_response_array_item_data
            )

            response_200.append(componentsschemas_user_response_array_item)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[List[UserResponse]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    group_name: Union[Unset, None, str] = UNSET,
    admin_data: Union[Unset, None, bool] = False,
) -> Response[List[UserResponse]]:
    """Get users

    Args:
        group_name (Union[Unset, None, str]):
        admin_data (Union[Unset, None, bool]):

    Returns:
        Response[List[UserResponse]]
    """

    kwargs = _get_kwargs(
        client=client,
        group_name=group_name,
        admin_data=admin_data,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    group_name: Union[Unset, None, str] = UNSET,
    admin_data: Union[Unset, None, bool] = False,
) -> Optional[List[UserResponse]]:
    """Get users

    Args:
        group_name (Union[Unset, None, str]):
        admin_data (Union[Unset, None, bool]):

    Returns:
        Response[List[UserResponse]]
    """

    return sync_detailed(
        client=client,
        group_name=group_name,
        admin_data=admin_data,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    group_name: Union[Unset, None, str] = UNSET,
    admin_data: Union[Unset, None, bool] = False,
) -> Response[List[UserResponse]]:
    """Get users

    Args:
        group_name (Union[Unset, None, str]):
        admin_data (Union[Unset, None, bool]):

    Returns:
        Response[List[UserResponse]]
    """

    kwargs = _get_kwargs(
        client=client,
        group_name=group_name,
        admin_data=admin_data,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    group_name: Union[Unset, None, str] = UNSET,
    admin_data: Union[Unset, None, bool] = False,
) -> Optional[List[UserResponse]]:
    """Get users

    Args:
        group_name (Union[Unset, None, str]):
        admin_data (Union[Unset, None, bool]):

    Returns:
        Response[List[UserResponse]]
    """

    return (
        await asyncio_detailed(
            client=client,
            group_name=group_name,
            admin_data=admin_data,
        )
    ).parsed
