from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.ack import Ack
from ...types import Response


def _get_kwargs(
    group_name: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/groups/{groupName}".format(client.base_url, groupName=group_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "patch",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Ack, Any]]:
    if response.status_code == 200:
        response_200 = Ack.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Ack, Any]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    group_name: str,
    *,
    client: Client,
) -> Response[Union[Ack, Any]]:
    """Update a users' group

    Args:
        group_name (str):

    Returns:
        Response[Union[Ack, Any]]
    """

    kwargs = _get_kwargs(
        group_name=group_name,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    group_name: str,
    *,
    client: Client,
) -> Optional[Union[Ack, Any]]:
    """Update a users' group

    Args:
        group_name (str):

    Returns:
        Response[Union[Ack, Any]]
    """

    return sync_detailed(
        group_name=group_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    group_name: str,
    *,
    client: Client,
) -> Response[Union[Ack, Any]]:
    """Update a users' group

    Args:
        group_name (str):

    Returns:
        Response[Union[Ack, Any]]
    """

    kwargs = _get_kwargs(
        group_name=group_name,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    group_name: str,
    *,
    client: Client,
) -> Optional[Union[Ack, Any]]:
    """Update a users' group

    Args:
        group_name (str):

    Returns:
        Response[Union[Ack, Any]]
    """

    return (
        await asyncio_detailed(
            group_name=group_name,
            client=client,
        )
    ).parsed
