from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.delete_group_result import DeleteGroupResult
from ...types import UNSET, Response, Unset


def _get_kwargs(
    group_name: str,
    *,
    client: Client,
    cascade: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/groups/{groupName}".format(client.base_url, groupName=group_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["cascade"] = cascade

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "delete",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, DeleteGroupResult]]:
    if response.status_code == 200:
        response_200 = DeleteGroupResult.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, DeleteGroupResult]]:
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
    cascade: Union[Unset, None, bool] = False,
) -> Response[Union[Any, DeleteGroupResult]]:
    """Delete users' group

    Args:
        group_name (str):
        cascade (Union[Unset, None, bool]):

    Returns:
        Response[Union[Any, DeleteGroupResult]]
    """

    kwargs = _get_kwargs(
        group_name=group_name,
        client=client,
        cascade=cascade,
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
    cascade: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, DeleteGroupResult]]:
    """Delete users' group

    Args:
        group_name (str):
        cascade (Union[Unset, None, bool]):

    Returns:
        Response[Union[Any, DeleteGroupResult]]
    """

    return sync_detailed(
        group_name=group_name,
        client=client,
        cascade=cascade,
    ).parsed


async def asyncio_detailed(
    group_name: str,
    *,
    client: Client,
    cascade: Union[Unset, None, bool] = False,
) -> Response[Union[Any, DeleteGroupResult]]:
    """Delete users' group

    Args:
        group_name (str):
        cascade (Union[Unset, None, bool]):

    Returns:
        Response[Union[Any, DeleteGroupResult]]
    """

    kwargs = _get_kwargs(
        group_name=group_name,
        client=client,
        cascade=cascade,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    group_name: str,
    *,
    client: Client,
    cascade: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, DeleteGroupResult]]:
    """Delete users' group

    Args:
        group_name (str):
        cascade (Union[Unset, None, bool]):

    Returns:
        Response[Union[Any, DeleteGroupResult]]
    """

    return (
        await asyncio_detailed(
            group_name=group_name,
            client=client,
            cascade=cascade,
        )
    ).parsed
