from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.corpus_metrics import CorpusMetrics
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
    facet: Union[Unset, None, str] = "",
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/corpusMetrics".format(client.base_url, projectName=project_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["facet"] = facet

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[CorpusMetrics]:
    if response.status_code == 200:
        response_200 = CorpusMetrics.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[CorpusMetrics]:
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
    facet: Union[Unset, None, str] = "",
) -> Response[CorpusMetrics]:
    """Get some metrics on corpus

    Args:
        project_name (str):
        facet (Union[Unset, None, str]):  Default: ''.

    Returns:
        Response[CorpusMetrics]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        facet=facet,
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
    facet: Union[Unset, None, str] = "",
) -> Optional[CorpusMetrics]:
    """Get some metrics on corpus

    Args:
        project_name (str):
        facet (Union[Unset, None, str]):  Default: ''.

    Returns:
        Response[CorpusMetrics]
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        facet=facet,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Client,
    facet: Union[Unset, None, str] = "",
) -> Response[CorpusMetrics]:
    """Get some metrics on corpus

    Args:
        project_name (str):
        facet (Union[Unset, None, str]):  Default: ''.

    Returns:
        Response[CorpusMetrics]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        facet=facet,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    project_name: str,
    *,
    client: Client,
    facet: Union[Unset, None, str] = "",
) -> Optional[CorpusMetrics]:
    """Get some metrics on corpus

    Args:
        project_name (str):
        facet (Union[Unset, None, str]):  Default: ''.

    Returns:
        Response[CorpusMetrics]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            facet=facet,
        )
    ).parsed
