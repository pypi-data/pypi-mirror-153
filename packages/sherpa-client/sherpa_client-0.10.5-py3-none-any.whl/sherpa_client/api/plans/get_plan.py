from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.named_annotation_plan import NamedAnnotationPlan
from ...types import Response


def _get_kwargs(
    project_name: str,
    name: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/plans/{name}".format(client.base_url, projectName=project_name, name=name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, NamedAnnotationPlan]]:
    if response.status_code == 200:
        response_200 = NamedAnnotationPlan.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, NamedAnnotationPlan]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    project_name: str,
    name: str,
    *,
    client: Client,
) -> Response[Union[Any, NamedAnnotationPlan]]:
    """Get a plan

    Args:
        project_name (str):
        name (str):

    Returns:
        Response[Union[Any, NamedAnnotationPlan]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        name=name,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    project_name: str,
    name: str,
    *,
    client: Client,
) -> Optional[Union[Any, NamedAnnotationPlan]]:
    """Get a plan

    Args:
        project_name (str):
        name (str):

    Returns:
        Response[Union[Any, NamedAnnotationPlan]]
    """

    return sync_detailed(
        project_name=project_name,
        name=name,
        client=client,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    name: str,
    *,
    client: Client,
) -> Response[Union[Any, NamedAnnotationPlan]]:
    """Get a plan

    Args:
        project_name (str):
        name (str):

    Returns:
        Response[Union[Any, NamedAnnotationPlan]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        name=name,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    project_name: str,
    name: str,
    *,
    client: Client,
) -> Optional[Union[Any, NamedAnnotationPlan]]:
    """Get a plan

    Args:
        project_name (str):
        name (str):

    Returns:
        Response[Union[Any, NamedAnnotationPlan]]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            name=name,
            client=client,
        )
    ).parsed
