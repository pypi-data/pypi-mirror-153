from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.sherpa_job_bean import SherpaJobBean
from ...types import UNSET, Response


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
    archive_name: str,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/_load_image".format(client.base_url, projectName=project_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["archiveName"] = archive_name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[SherpaJobBean]:
    if response.status_code == 200:
        response_200 = SherpaJobBean.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[SherpaJobBean]:
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
    archive_name: str,
) -> Response[SherpaJobBean]:
    """restore a project from a known image

    Args:
        project_name (str):
        archive_name (str):

    Returns:
        Response[SherpaJobBean]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        archive_name=archive_name,
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
    archive_name: str,
) -> Optional[SherpaJobBean]:
    """restore a project from a known image

    Args:
        project_name (str):
        archive_name (str):

    Returns:
        Response[SherpaJobBean]
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        archive_name=archive_name,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Client,
    archive_name: str,
) -> Response[SherpaJobBean]:
    """restore a project from a known image

    Args:
        project_name (str):
        archive_name (str):

    Returns:
        Response[SherpaJobBean]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        archive_name=archive_name,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    project_name: str,
    *,
    client: Client,
    archive_name: str,
) -> Optional[SherpaJobBean]:
    """restore a project from a known image

    Args:
        project_name (str):
        archive_name (str):

    Returns:
        Response[SherpaJobBean]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            archive_name=archive_name,
        )
    ).parsed
