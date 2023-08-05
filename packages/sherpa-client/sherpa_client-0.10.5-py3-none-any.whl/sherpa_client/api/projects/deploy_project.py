from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.project_status import ProjectStatus
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: Client,
    project_name: str,
) -> Dict[str, Any]:
    url = "{}/projects/_deploy".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["projectName"] = project_name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
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
    project_name: str,
) -> Response[Union[Any, ProjectStatus]]:
    """deploy an already existing project

    Args:
        project_name (str):

    Returns:
        Response[Union[Any, ProjectStatus]]
    """

    kwargs = _get_kwargs(
        client=client,
        project_name=project_name,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    project_name: str,
) -> Optional[Union[Any, ProjectStatus]]:
    """deploy an already existing project

    Args:
        project_name (str):

    Returns:
        Response[Union[Any, ProjectStatus]]
    """

    return sync_detailed(
        client=client,
        project_name=project_name,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    project_name: str,
) -> Response[Union[Any, ProjectStatus]]:
    """deploy an already existing project

    Args:
        project_name (str):

    Returns:
        Response[Union[Any, ProjectStatus]]
    """

    kwargs = _get_kwargs(
        client=client,
        project_name=project_name,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    project_name: str,
) -> Optional[Union[Any, ProjectStatus]]:
    """deploy an already existing project

    Args:
        project_name (str):

    Returns:
        Response[Union[Any, ProjectStatus]]
    """

    return (
        await asyncio_detailed(
            client=client,
            project_name=project_name,
        )
    ).parsed
