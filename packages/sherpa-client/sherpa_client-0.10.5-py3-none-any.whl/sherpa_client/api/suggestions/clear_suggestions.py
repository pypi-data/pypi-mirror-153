from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.operation_count import OperationCount
from ...types import Response


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/suggestions/_clear".format(client.base_url, projectName=project_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[OperationCount]:
    if response.status_code == 200:
        response_200 = OperationCount.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[OperationCount]:
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
) -> Response[OperationCount]:
    """Remove all suggestions from the dataset

    Args:
        project_name (str):

    Returns:
        Response[OperationCount]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
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
) -> Optional[OperationCount]:
    """Remove all suggestions from the dataset

    Args:
        project_name (str):

    Returns:
        Response[OperationCount]
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Client,
) -> Response[OperationCount]:
    """Remove all suggestions from the dataset

    Args:
        project_name (str):

    Returns:
        Response[OperationCount]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    project_name: str,
    *,
    client: Client,
) -> Optional[OperationCount]:
    """Remove all suggestions from the dataset

    Args:
        project_name (str):

    Returns:
        Response[OperationCount]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
        )
    ).parsed
