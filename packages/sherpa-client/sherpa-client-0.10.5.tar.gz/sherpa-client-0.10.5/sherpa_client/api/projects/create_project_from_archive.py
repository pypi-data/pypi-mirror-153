from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.create_project_from_archive_multipart_data import CreateProjectFromArchiveMultipartData
from ...models.sherpa_job_bean import SherpaJobBean
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    multipart_data: CreateProjectFromArchiveMultipartData,
    group_name: Union[Unset, None, str] = UNSET,
    reuse_project_name: Union[Unset, None, bool] = False,
    project_name: Union[Unset, None, str] = UNSET,
    project_label: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/projects/_import".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["groupName"] = group_name

    params["reuseProjectName"] = reuse_project_name

    params["projectName"] = project_name

    params["projectLabel"] = project_label

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    multipart_multipart_data = multipart_data.to_multipart()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "files": multipart_multipart_data,
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
    *,
    client: Client,
    multipart_data: CreateProjectFromArchiveMultipartData,
    group_name: Union[Unset, None, str] = UNSET,
    reuse_project_name: Union[Unset, None, bool] = False,
    project_name: Union[Unset, None, str] = UNSET,
    project_label: Union[Unset, None, str] = UNSET,
) -> Response[SherpaJobBean]:
    """create a project from an archive

    Args:
        group_name (Union[Unset, None, str]):
        reuse_project_name (Union[Unset, None, bool]):
        project_name (Union[Unset, None, str]):
        project_label (Union[Unset, None, str]):
        multipart_data (CreateProjectFromArchiveMultipartData):

    Returns:
        Response[SherpaJobBean]
    """

    kwargs = _get_kwargs(
        client=client,
        multipart_data=multipart_data,
        group_name=group_name,
        reuse_project_name=reuse_project_name,
        project_name=project_name,
        project_label=project_label,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    multipart_data: CreateProjectFromArchiveMultipartData,
    group_name: Union[Unset, None, str] = UNSET,
    reuse_project_name: Union[Unset, None, bool] = False,
    project_name: Union[Unset, None, str] = UNSET,
    project_label: Union[Unset, None, str] = UNSET,
) -> Optional[SherpaJobBean]:
    """create a project from an archive

    Args:
        group_name (Union[Unset, None, str]):
        reuse_project_name (Union[Unset, None, bool]):
        project_name (Union[Unset, None, str]):
        project_label (Union[Unset, None, str]):
        multipart_data (CreateProjectFromArchiveMultipartData):

    Returns:
        Response[SherpaJobBean]
    """

    return sync_detailed(
        client=client,
        multipart_data=multipart_data,
        group_name=group_name,
        reuse_project_name=reuse_project_name,
        project_name=project_name,
        project_label=project_label,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    multipart_data: CreateProjectFromArchiveMultipartData,
    group_name: Union[Unset, None, str] = UNSET,
    reuse_project_name: Union[Unset, None, bool] = False,
    project_name: Union[Unset, None, str] = UNSET,
    project_label: Union[Unset, None, str] = UNSET,
) -> Response[SherpaJobBean]:
    """create a project from an archive

    Args:
        group_name (Union[Unset, None, str]):
        reuse_project_name (Union[Unset, None, bool]):
        project_name (Union[Unset, None, str]):
        project_label (Union[Unset, None, str]):
        multipart_data (CreateProjectFromArchiveMultipartData):

    Returns:
        Response[SherpaJobBean]
    """

    kwargs = _get_kwargs(
        client=client,
        multipart_data=multipart_data,
        group_name=group_name,
        reuse_project_name=reuse_project_name,
        project_name=project_name,
        project_label=project_label,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    multipart_data: CreateProjectFromArchiveMultipartData,
    group_name: Union[Unset, None, str] = UNSET,
    reuse_project_name: Union[Unset, None, bool] = False,
    project_name: Union[Unset, None, str] = UNSET,
    project_label: Union[Unset, None, str] = UNSET,
) -> Optional[SherpaJobBean]:
    """create a project from an archive

    Args:
        group_name (Union[Unset, None, str]):
        reuse_project_name (Union[Unset, None, bool]):
        project_name (Union[Unset, None, str]):
        project_label (Union[Unset, None, str]):
        multipart_data (CreateProjectFromArchiveMultipartData):

    Returns:
        Response[SherpaJobBean]
    """

    return (
        await asyncio_detailed(
            client=client,
            multipart_data=multipart_data,
            group_name=group_name,
            reuse_project_name=reuse_project_name,
            project_name=project_name,
            project_label=project_label,
        )
    ).parsed
