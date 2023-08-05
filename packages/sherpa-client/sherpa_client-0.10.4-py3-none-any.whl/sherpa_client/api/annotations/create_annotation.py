from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.annotation import Annotation
from ...models.annotation_id import AnnotationId
from ...types import Response


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
    json_body: Annotation,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/annotations".format(client.base_url, projectName=project_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[AnnotationId]:
    if response.status_code == 200:
        response_200 = AnnotationId.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[AnnotationId]:
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
    json_body: Annotation,
) -> Response[AnnotationId]:
    """Add an annotation into the dataset

    Args:
        project_name (str):
        json_body (Annotation): A document annotation

    Returns:
        Response[AnnotationId]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        json_body=json_body,
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
    json_body: Annotation,
) -> Optional[AnnotationId]:
    """Add an annotation into the dataset

    Args:
        project_name (str):
        json_body (Annotation): A document annotation

    Returns:
        Response[AnnotationId]
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Client,
    json_body: Annotation,
) -> Response[AnnotationId]:
    """Add an annotation into the dataset

    Args:
        project_name (str):
        json_body (Annotation): A document annotation

    Returns:
        Response[AnnotationId]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    project_name: str,
    *,
    client: Client,
    json_body: Annotation,
) -> Optional[AnnotationId]:
    """Add an annotation into the dataset

    Args:
        project_name (str):
        json_body (Annotation): A document annotation

    Returns:
        Response[AnnotationId]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            json_body=json_body,
        )
    ).parsed
