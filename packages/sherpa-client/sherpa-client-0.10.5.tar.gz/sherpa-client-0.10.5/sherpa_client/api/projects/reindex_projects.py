from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.sherpa_job_bean import SherpaJobBean
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    wait: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/projects/_reindex".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["wait"] = wait

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
    *,
    client: Client,
    wait: Union[Unset, None, bool] = False,
) -> Response[SherpaJobBean]:
    """reindex all projects

    Args:
        wait (Union[Unset, None, bool]):

    Returns:
        Response[SherpaJobBean]
    """

    kwargs = _get_kwargs(
        client=client,
        wait=wait,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    wait: Union[Unset, None, bool] = False,
) -> Optional[SherpaJobBean]:
    """reindex all projects

    Args:
        wait (Union[Unset, None, bool]):

    Returns:
        Response[SherpaJobBean]
    """

    return sync_detailed(
        client=client,
        wait=wait,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    wait: Union[Unset, None, bool] = False,
) -> Response[SherpaJobBean]:
    """reindex all projects

    Args:
        wait (Union[Unset, None, bool]):

    Returns:
        Response[SherpaJobBean]
    """

    kwargs = _get_kwargs(
        client=client,
        wait=wait,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    wait: Union[Unset, None, bool] = False,
) -> Optional[SherpaJobBean]:
    """reindex all projects

    Args:
        wait (Union[Unset, None, bool]):

    Returns:
        Response[SherpaJobBean]
    """

    return (
        await asyncio_detailed(
            client=client,
            wait=wait,
        )
    ).parsed
