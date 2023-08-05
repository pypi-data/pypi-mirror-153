from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.delete_response import DeleteResponse
from ...types import Response


def _get_kwargs(
    project_name: str,
    label_name: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/labels/{labelName}".format(
        client.base_url, projectName=project_name, labelName=label_name
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, DeleteResponse]]:
    if response.status_code == 200:
        response_200 = DeleteResponse.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, DeleteResponse]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    project_name: str,
    label_name: str,
    *,
    client: Client,
) -> Response[Union[Any, DeleteResponse]]:
    """Remove label by name

    Args:
        project_name (str):
        label_name (str):

    Returns:
        Response[Union[Any, DeleteResponse]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        label_name=label_name,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    project_name: str,
    label_name: str,
    *,
    client: Client,
) -> Optional[Union[Any, DeleteResponse]]:
    """Remove label by name

    Args:
        project_name (str):
        label_name (str):

    Returns:
        Response[Union[Any, DeleteResponse]]
    """

    return sync_detailed(
        project_name=project_name,
        label_name=label_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    label_name: str,
    *,
    client: Client,
) -> Response[Union[Any, DeleteResponse]]:
    """Remove label by name

    Args:
        project_name (str):
        label_name (str):

    Returns:
        Response[Union[Any, DeleteResponse]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        label_name=label_name,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    project_name: str,
    label_name: str,
    *,
    client: Client,
) -> Optional[Union[Any, DeleteResponse]]:
    """Remove label by name

    Args:
        project_name (str):
        label_name (str):

    Returns:
        Response[Union[Any, DeleteResponse]]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            label_name=label_name,
            client=client,
        )
    ).parsed
