from typing import Any, Dict, List, Optional

import httpx

from ...client import Client
from ...models.group_share import GroupShare
from ...types import Response


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/shares/groups".format(client.base_url, projectName=project_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[List[GroupShare]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_group_share_array_item_data in _response_200:
            componentsschemas_group_share_array_item = GroupShare.from_dict(
                componentsschemas_group_share_array_item_data
            )

            response_200.append(componentsschemas_group_share_array_item)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[List[GroupShare]]:
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
) -> Response[List[GroupShare]]:
    """List of groups shares of the project

    Args:
        project_name (str):

    Returns:
        Response[List[GroupShare]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
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
) -> Optional[List[GroupShare]]:
    """List of groups shares of the project

    Args:
        project_name (str):

    Returns:
        Response[List[GroupShare]]
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Client,
) -> Response[List[GroupShare]]:
    """List of groups shares of the project

    Args:
        project_name (str):

    Returns:
        Response[List[GroupShare]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    project_name: str,
    *,
    client: Client,
) -> Optional[List[GroupShare]]:
    """List of groups shares of the project

    Args:
        project_name (str):

    Returns:
        Response[List[GroupShare]]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
        )
    ).parsed
