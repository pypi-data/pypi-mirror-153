from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.sherpa_job_bean import SherpaJobBean
from ...types import Response


def _get_kwargs(
    project_name: str,
    job_id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/job/{job_id}/_wait".format(
        client.base_url, projectName=project_name, job_id=job_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, SherpaJobBean]]:
    if response.status_code == 200:
        response_200 = SherpaJobBean.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, SherpaJobBean]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    project_name: str,
    job_id: str,
    *,
    client: Client,
) -> Response[Union[Any, SherpaJobBean]]:
    """Wait for the job to end before returning job information

    Args:
        project_name (str):
        job_id (str):

    Returns:
        Response[Union[Any, SherpaJobBean]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        job_id=job_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    project_name: str,
    job_id: str,
    *,
    client: Client,
) -> Optional[Union[Any, SherpaJobBean]]:
    """Wait for the job to end before returning job information

    Args:
        project_name (str):
        job_id (str):

    Returns:
        Response[Union[Any, SherpaJobBean]]
    """

    return sync_detailed(
        project_name=project_name,
        job_id=job_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    job_id: str,
    *,
    client: Client,
) -> Response[Union[Any, SherpaJobBean]]:
    """Wait for the job to end before returning job information

    Args:
        project_name (str):
        job_id (str):

    Returns:
        Response[Union[Any, SherpaJobBean]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        job_id=job_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    project_name: str,
    job_id: str,
    *,
    client: Client,
) -> Optional[Union[Any, SherpaJobBean]]:
    """Wait for the job to end before returning job information

    Args:
        project_name (str):
        job_id (str):

    Returns:
        Response[Union[Any, SherpaJobBean]]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            job_id=job_id,
            client=client,
        )
    ).parsed
