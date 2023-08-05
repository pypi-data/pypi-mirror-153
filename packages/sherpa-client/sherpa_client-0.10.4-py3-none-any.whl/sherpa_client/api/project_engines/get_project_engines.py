from typing import Any, Dict, List, Optional, cast

import httpx

from ...client import Client
from ...types import UNSET, Response


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
    type: str,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/engines".format(client.base_url, projectName=project_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["type"] = type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[List[str]]:
    if response.status_code == 200:
        response_200 = cast(List[str], response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[List[str]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    project_name: str,
    *,
    client: Client,
    type: str,
) -> Response[List[str]]:
    """Filter the list of engines available for this project

    Args:
        project_name (str):
        type (str):

    Returns:
        Response[List[str]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        type=type,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    project_name: str,
    *,
    client: Client,
    type: str,
) -> Optional[List[str]]:
    """Filter the list of engines available for this project

    Args:
        project_name (str):
        type (str):

    Returns:
        Response[List[str]]
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        type=type,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Client,
    type: str,
) -> Response[List[str]]:
    """Filter the list of engines available for this project

    Args:
        project_name (str):
        type (str):

    Returns:
        Response[List[str]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        type=type,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    project_name: str,
    *,
    client: Client,
    type: str,
) -> Optional[List[str]]:
    """Filter the list of engines available for this project

    Args:
        project_name (str):
        type (str):

    Returns:
        Response[List[str]]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            type=type,
        )
    ).parsed
