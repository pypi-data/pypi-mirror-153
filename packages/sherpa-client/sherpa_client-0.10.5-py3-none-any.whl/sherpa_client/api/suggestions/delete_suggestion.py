from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.ack import Ack
from ...types import Response


def _get_kwargs(
    project_name: str,
    suggestion_id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/suggestions/{suggestionId}".format(
        client.base_url, projectName=project_name, suggestionId=suggestion_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "delete",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Ack, Any]]:
    if response.status_code == 200:
        response_200 = Ack.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Ack, Any]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    project_name: str,
    suggestion_id: str,
    *,
    client: Client,
) -> Response[Union[Ack, Any]]:
    """Delete a suggestion from the dataset

    Args:
        project_name (str):
        suggestion_id (str):

    Returns:
        Response[Union[Ack, Any]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        suggestion_id=suggestion_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    project_name: str,
    suggestion_id: str,
    *,
    client: Client,
) -> Optional[Union[Ack, Any]]:
    """Delete a suggestion from the dataset

    Args:
        project_name (str):
        suggestion_id (str):

    Returns:
        Response[Union[Ack, Any]]
    """

    return sync_detailed(
        project_name=project_name,
        suggestion_id=suggestion_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    suggestion_id: str,
    *,
    client: Client,
) -> Response[Union[Ack, Any]]:
    """Delete a suggestion from the dataset

    Args:
        project_name (str):
        suggestion_id (str):

    Returns:
        Response[Union[Ack, Any]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        suggestion_id=suggestion_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    project_name: str,
    suggestion_id: str,
    *,
    client: Client,
) -> Optional[Union[Ack, Any]]:
    """Delete a suggestion from the dataset

    Args:
        project_name (str):
        suggestion_id (str):

    Returns:
        Response[Union[Ack, Any]]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            suggestion_id=suggestion_id,
            client=client,
        )
    ).parsed
