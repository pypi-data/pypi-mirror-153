from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.sherpa_job_bean import SherpaJobBean
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
    job_desc: Union[Unset, None, str] = "All work and no play makes Jack a dull boy",
    timeout: Union[Unset, None, int] = 60,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/job".format(client.base_url, projectName=project_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["job_desc"] = job_desc

    params["timeout"] = timeout

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
    job_desc: Union[Unset, None, str] = "All work and no play makes Jack a dull boy",
    timeout: Union[Unset, None, int] = 60,
) -> Response[SherpaJobBean]:
    """create a dummy job

    Args:
        project_name (str):
        job_desc (Union[Unset, None, str]):  Default: 'All work and no play makes Jack a dull
            boy'.
        timeout (Union[Unset, None, int]):  Default: 60.

    Returns:
        Response[SherpaJobBean]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        job_desc=job_desc,
        timeout=timeout,
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
    job_desc: Union[Unset, None, str] = "All work and no play makes Jack a dull boy",
    timeout: Union[Unset, None, int] = 60,
) -> Optional[SherpaJobBean]:
    """create a dummy job

    Args:
        project_name (str):
        job_desc (Union[Unset, None, str]):  Default: 'All work and no play makes Jack a dull
            boy'.
        timeout (Union[Unset, None, int]):  Default: 60.

    Returns:
        Response[SherpaJobBean]
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        job_desc=job_desc,
        timeout=timeout,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Client,
    job_desc: Union[Unset, None, str] = "All work and no play makes Jack a dull boy",
    timeout: Union[Unset, None, int] = 60,
) -> Response[SherpaJobBean]:
    """create a dummy job

    Args:
        project_name (str):
        job_desc (Union[Unset, None, str]):  Default: 'All work and no play makes Jack a dull
            boy'.
        timeout (Union[Unset, None, int]):  Default: 60.

    Returns:
        Response[SherpaJobBean]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        job_desc=job_desc,
        timeout=timeout,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    project_name: str,
    *,
    client: Client,
    job_desc: Union[Unset, None, str] = "All work and no play makes Jack a dull boy",
    timeout: Union[Unset, None, int] = 60,
) -> Optional[SherpaJobBean]:
    """create a dummy job

    Args:
        project_name (str):
        job_desc (Union[Unset, None, str]):  Default: 'All work and no play makes Jack a dull
            boy'.
        timeout (Union[Unset, None, int]):  Default: 60.

    Returns:
        Response[SherpaJobBean]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            job_desc=job_desc,
            timeout=timeout,
        )
    ).parsed
