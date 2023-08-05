from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.project_status import ProjectStatus
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/projects/_stop_tour".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, ProjectStatus]]:
    if response.status_code == 200:
        response_200 = ProjectStatus.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, ProjectStatus]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
) -> Response[Union[Any, ProjectStatus]]:
    """stop and remove the tour for the current user

    Returns:
        Response[Union[Any, ProjectStatus]]
    """

    kwargs = _get_kwargs(
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
) -> Optional[Union[Any, ProjectStatus]]:
    """stop and remove the tour for the current user

    Returns:
        Response[Union[Any, ProjectStatus]]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
) -> Response[Union[Any, ProjectStatus]]:
    """stop and remove the tour for the current user

    Returns:
        Response[Union[Any, ProjectStatus]]
    """

    kwargs = _get_kwargs(
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
) -> Optional[Union[Any, ProjectStatus]]:
    """stop and remove the tour for the current user

    Returns:
        Response[Union[Any, ProjectStatus]]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
