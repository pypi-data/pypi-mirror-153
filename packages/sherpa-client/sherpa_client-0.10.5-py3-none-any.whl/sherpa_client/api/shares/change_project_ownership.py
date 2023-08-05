from typing import Any, Dict

import httpx

from ...client import Client
from ...types import UNSET, Response


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
    username: str,
    group_name: str,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/_chown".format(client.base_url, projectName=project_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["username"] = username

    params["groupName"] = group_name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    project_name: str,
    *,
    client: Client,
    username: str,
    group_name: str,
) -> Response[Any]:
    """Change the ownership of the project (user and group)

    Args:
        project_name (str):
        username (str):
        group_name (str):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        username=username,
        group_name=group_name,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    project_name: str,
    *,
    client: Client,
    username: str,
    group_name: str,
) -> Response[Any]:
    """Change the ownership of the project (user and group)

    Args:
        project_name (str):
        username (str):
        group_name (str):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        username=username,
        group_name=group_name,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
