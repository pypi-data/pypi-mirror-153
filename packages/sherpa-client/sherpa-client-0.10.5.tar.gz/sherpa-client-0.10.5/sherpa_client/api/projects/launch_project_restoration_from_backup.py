from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.launch_project_restoration_from_backup_multipart_data import (
    LaunchProjectRestorationFromBackupMultipartData,
)
from ...models.sherpa_job_bean import SherpaJobBean
from ...types import Response


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
    multipart_data: LaunchProjectRestorationFromBackupMultipartData,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/_restore".format(client.base_url, projectName=project_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    multipart_multipart_data = multipart_data.to_multipart()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "files": multipart_multipart_data,
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
    multipart_data: LaunchProjectRestorationFromBackupMultipartData,
) -> Response[SherpaJobBean]:
    """restore a project from backup

    Args:
        project_name (str):
        multipart_data (LaunchProjectRestorationFromBackupMultipartData):

    Returns:
        Response[SherpaJobBean]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        multipart_data=multipart_data,
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
    multipart_data: LaunchProjectRestorationFromBackupMultipartData,
) -> Optional[SherpaJobBean]:
    """restore a project from backup

    Args:
        project_name (str):
        multipart_data (LaunchProjectRestorationFromBackupMultipartData):

    Returns:
        Response[SherpaJobBean]
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        multipart_data=multipart_data,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Client,
    multipart_data: LaunchProjectRestorationFromBackupMultipartData,
) -> Response[SherpaJobBean]:
    """restore a project from backup

    Args:
        project_name (str):
        multipart_data (LaunchProjectRestorationFromBackupMultipartData):

    Returns:
        Response[SherpaJobBean]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        multipart_data=multipart_data,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    project_name: str,
    *,
    client: Client,
    multipart_data: LaunchProjectRestorationFromBackupMultipartData,
) -> Optional[SherpaJobBean]:
    """restore a project from backup

    Args:
        project_name (str):
        multipart_data (LaunchProjectRestorationFromBackupMultipartData):

    Returns:
        Response[SherpaJobBean]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            multipart_data=multipart_data,
        )
    ).parsed
