from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.category_id import CategoryId
from ...types import Response


def _get_kwargs(
    project_name: str,
    category_id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/categories/{categoryId}".format(
        client.base_url, projectName=project_name, categoryId=category_id
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, CategoryId]]:
    if response.status_code == 200:
        response_200 = CategoryId.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, CategoryId]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    project_name: str,
    category_id: str,
    *,
    client: Client,
) -> Response[Union[Any, CategoryId]]:
    """Delete a document category

    Args:
        project_name (str):
        category_id (str):

    Returns:
        Response[Union[Any, CategoryId]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        category_id=category_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    project_name: str,
    category_id: str,
    *,
    client: Client,
) -> Optional[Union[Any, CategoryId]]:
    """Delete a document category

    Args:
        project_name (str):
        category_id (str):

    Returns:
        Response[Union[Any, CategoryId]]
    """

    return sync_detailed(
        project_name=project_name,
        category_id=category_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    category_id: str,
    *,
    client: Client,
) -> Response[Union[Any, CategoryId]]:
    """Delete a document category

    Args:
        project_name (str):
        category_id (str):

    Returns:
        Response[Union[Any, CategoryId]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        category_id=category_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    project_name: str,
    category_id: str,
    *,
    client: Client,
) -> Optional[Union[Any, CategoryId]]:
    """Delete a document category

    Args:
        project_name (str):
        category_id (str):

    Returns:
        Response[Union[Any, CategoryId]]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            category_id=category_id,
            client=client,
        )
    ).parsed
