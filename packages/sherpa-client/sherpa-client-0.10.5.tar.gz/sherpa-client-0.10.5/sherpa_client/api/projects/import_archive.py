from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.engine_config_import_summary import EngineConfigImportSummary
from ...models.import_archive_multipart_data import ImportArchiveMultipartData
from ...types import Response


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
    multipart_data: ImportArchiveMultipartData,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/gazetteers/_import".format(client.base_url, projectName=project_name)

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


def _parse_response(*, response: httpx.Response) -> Optional[EngineConfigImportSummary]:
    if response.status_code == 200:
        response_200 = EngineConfigImportSummary.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[EngineConfigImportSummary]:
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
    multipart_data: ImportArchiveMultipartData,
) -> Response[EngineConfigImportSummary]:
    """import a gazetteer archive

    Args:
        project_name (str):
        multipart_data (ImportArchiveMultipartData):

    Returns:
        Response[EngineConfigImportSummary]
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
    multipart_data: ImportArchiveMultipartData,
) -> Optional[EngineConfigImportSummary]:
    """import a gazetteer archive

    Args:
        project_name (str):
        multipart_data (ImportArchiveMultipartData):

    Returns:
        Response[EngineConfigImportSummary]
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
    multipart_data: ImportArchiveMultipartData,
) -> Response[EngineConfigImportSummary]:
    """import a gazetteer archive

    Args:
        project_name (str):
        multipart_data (ImportArchiveMultipartData):

    Returns:
        Response[EngineConfigImportSummary]
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
    multipart_data: ImportArchiveMultipartData,
) -> Optional[EngineConfigImportSummary]:
    """import a gazetteer archive

    Args:
        project_name (str):
        multipart_data (ImportArchiveMultipartData):

    Returns:
        Response[EngineConfigImportSummary]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            multipart_data=multipart_data,
        )
    ).parsed
