from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.new_role import NewRole
from ...models.role_desc import RoleDesc
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    json_body: NewRole,
    group_name: Union[Unset, None, str] = "",
    restricted: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/roles".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["groupName"] = group_name

    params["restricted"] = restricted

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


def _parse_response(*, response: httpx.Response) -> Optional[RoleDesc]:
    if response.status_code == 200:
        response_200 = RoleDesc.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[RoleDesc]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: NewRole,
    group_name: Union[Unset, None, str] = "",
    restricted: Union[Unset, None, bool] = False,
) -> Response[RoleDesc]:
    """Create role

    Args:
        group_name (Union[Unset, None, str]):  Default: ''.
        restricted (Union[Unset, None, bool]):
        json_body (NewRole):

    Returns:
        Response[RoleDesc]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        group_name=group_name,
        restricted=restricted,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    json_body: NewRole,
    group_name: Union[Unset, None, str] = "",
    restricted: Union[Unset, None, bool] = False,
) -> Optional[RoleDesc]:
    """Create role

    Args:
        group_name (Union[Unset, None, str]):  Default: ''.
        restricted (Union[Unset, None, bool]):
        json_body (NewRole):

    Returns:
        Response[RoleDesc]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        group_name=group_name,
        restricted=restricted,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: NewRole,
    group_name: Union[Unset, None, str] = "",
    restricted: Union[Unset, None, bool] = False,
) -> Response[RoleDesc]:
    """Create role

    Args:
        group_name (Union[Unset, None, str]):  Default: ''.
        restricted (Union[Unset, None, bool]):
        json_body (NewRole):

    Returns:
        Response[RoleDesc]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        group_name=group_name,
        restricted=restricted,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    json_body: NewRole,
    group_name: Union[Unset, None, str] = "",
    restricted: Union[Unset, None, bool] = False,
) -> Optional[RoleDesc]:
    """Create role

    Args:
        group_name (Union[Unset, None, str]):  Default: ''.
        restricted (Union[Unset, None, bool]):
        json_body (NewRole):

    Returns:
        Response[RoleDesc]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            group_name=group_name,
            restricted=restricted,
        )
    ).parsed
