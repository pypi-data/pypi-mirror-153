from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.lexicon import Lexicon
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    lexicon_name: str,
    *,
    client: Client,
    compute_metrics: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/lexicons/{lexiconName}".format(
        client.base_url, projectName=project_name, lexiconName=lexicon_name
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["computeMetrics"] = compute_metrics

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, Lexicon]]:
    if response.status_code == 200:
        response_200 = Lexicon.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, Lexicon]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    project_name: str,
    lexicon_name: str,
    *,
    client: Client,
    compute_metrics: Union[Unset, None, bool] = False,
) -> Response[Union[Any, Lexicon]]:
    """Get a lexicon

    Args:
        project_name (str):
        lexicon_name (str):
        compute_metrics (Union[Unset, None, bool]):

    Returns:
        Response[Union[Any, Lexicon]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        lexicon_name=lexicon_name,
        client=client,
        compute_metrics=compute_metrics,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    project_name: str,
    lexicon_name: str,
    *,
    client: Client,
    compute_metrics: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, Lexicon]]:
    """Get a lexicon

    Args:
        project_name (str):
        lexicon_name (str):
        compute_metrics (Union[Unset, None, bool]):

    Returns:
        Response[Union[Any, Lexicon]]
    """

    return sync_detailed(
        project_name=project_name,
        lexicon_name=lexicon_name,
        client=client,
        compute_metrics=compute_metrics,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    lexicon_name: str,
    *,
    client: Client,
    compute_metrics: Union[Unset, None, bool] = False,
) -> Response[Union[Any, Lexicon]]:
    """Get a lexicon

    Args:
        project_name (str):
        lexicon_name (str):
        compute_metrics (Union[Unset, None, bool]):

    Returns:
        Response[Union[Any, Lexicon]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        lexicon_name=lexicon_name,
        client=client,
        compute_metrics=compute_metrics,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    project_name: str,
    lexicon_name: str,
    *,
    client: Client,
    compute_metrics: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, Lexicon]]:
    """Get a lexicon

    Args:
        project_name (str):
        lexicon_name (str):
        compute_metrics (Union[Unset, None, bool]):

    Returns:
        Response[Union[Any, Lexicon]]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            lexicon_name=lexicon_name,
            client=client,
            compute_metrics=compute_metrics,
        )
    ).parsed
