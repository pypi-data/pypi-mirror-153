from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
    indices: Union[Unset, None, str] = "*",
    timeout_millis: Union[Unset, None, int] = 1500,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/_flush".format(client.base_url, projectName=project_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["indices"] = indices

    params["timeoutMillis"] = timeout_millis

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
    indices: Union[Unset, None, str] = "*",
    timeout_millis: Union[Unset, None, int] = 1500,
) -> Response[Any]:
    """flush search indices of the project

    Args:
        project_name (str):
        indices (Union[Unset, None, str]):  Default: '*'.
        timeout_millis (Union[Unset, None, int]):  Default: 1500.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        indices=indices,
        timeout_millis=timeout_millis,
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
    indices: Union[Unset, None, str] = "*",
    timeout_millis: Union[Unset, None, int] = 1500,
) -> Response[Any]:
    """flush search indices of the project

    Args:
        project_name (str):
        indices (Union[Unset, None, str]):  Default: '*'.
        timeout_millis (Union[Unset, None, int]):  Default: 1500.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        indices=indices,
        timeout_millis=timeout_millis,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
