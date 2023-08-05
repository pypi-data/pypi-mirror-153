from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.role_desc import RoleDesc
from ...types import Response


def _get_kwargs(
    rolename: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/roles/{rolename}".format(client.base_url, rolename=rolename)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, RoleDesc]]:
    if response.status_code == 200:
        response_200 = RoleDesc.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, RoleDesc]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    rolename: str,
    *,
    client: Client,
) -> Response[Union[Any, RoleDesc]]:
    """Get role

    Args:
        rolename (str):

    Returns:
        Response[Union[Any, RoleDesc]]
    """

    kwargs = _get_kwargs(
        rolename=rolename,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    rolename: str,
    *,
    client: Client,
) -> Optional[Union[Any, RoleDesc]]:
    """Get role

    Args:
        rolename (str):

    Returns:
        Response[Union[Any, RoleDesc]]
    """

    return sync_detailed(
        rolename=rolename,
        client=client,
    ).parsed


async def asyncio_detailed(
    rolename: str,
    *,
    client: Client,
) -> Response[Union[Any, RoleDesc]]:
    """Get role

    Args:
        rolename (str):

    Returns:
        Response[Union[Any, RoleDesc]]
    """

    kwargs = _get_kwargs(
        rolename=rolename,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    rolename: str,
    *,
    client: Client,
) -> Optional[Union[Any, RoleDesc]]:
    """Get role

    Args:
        rolename (str):

    Returns:
        Response[Union[Any, RoleDesc]]
    """

    return (
        await asyncio_detailed(
            rolename=rolename,
            client=client,
        )
    ).parsed
