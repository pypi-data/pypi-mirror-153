from io import BytesIO
from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...types import UNSET, File, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
    experiments: Union[Unset, None, str] = UNSET,
    favorite: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/_export_models".format(client.base_url, projectName=project_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["experiments"] = experiments

    params["favorite"] = favorite

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[File]:
    if response.status_code == 200:
        response_200 = File(payload=BytesIO(response.content))

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[File]:
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
    experiments: Union[Unset, None, str] = UNSET,
    favorite: Union[Unset, None, bool] = False,
) -> Response[File]:
    """export models of the project

    Args:
        project_name (str):
        experiments (Union[Unset, None, str]):
        favorite (Union[Unset, None, bool]):

    Returns:
        Response[File]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        experiments=experiments,
        favorite=favorite,
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
    experiments: Union[Unset, None, str] = UNSET,
    favorite: Union[Unset, None, bool] = False,
) -> Optional[File]:
    """export models of the project

    Args:
        project_name (str):
        experiments (Union[Unset, None, str]):
        favorite (Union[Unset, None, bool]):

    Returns:
        Response[File]
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        experiments=experiments,
        favorite=favorite,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Client,
    experiments: Union[Unset, None, str] = UNSET,
    favorite: Union[Unset, None, bool] = False,
) -> Response[File]:
    """export models of the project

    Args:
        project_name (str):
        experiments (Union[Unset, None, str]):
        favorite (Union[Unset, None, bool]):

    Returns:
        Response[File]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        experiments=experiments,
        favorite=favorite,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    project_name: str,
    *,
    client: Client,
    experiments: Union[Unset, None, str] = UNSET,
    favorite: Union[Unset, None, bool] = False,
) -> Optional[File]:
    """export models of the project

    Args:
        project_name (str):
        experiments (Union[Unset, None, str]):
        favorite (Union[Unset, None, bool]):

    Returns:
        Response[File]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            experiments=experiments,
            favorite=favorite,
        )
    ).parsed
