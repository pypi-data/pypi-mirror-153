from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.label import Label
from ...models.label_update import LabelUpdate
from ...types import Response


def _get_kwargs(
    project_name: str,
    label_name: str,
    *,
    client: Client,
    json_body: LabelUpdate,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/labels/{labelName}".format(
        client.base_url, projectName=project_name, labelName=label_name
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Label]:
    if response.status_code == 200:
        response_200 = Label.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Label]:
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
    json_body: LabelUpdate,
) -> Response[Label]:
    """Update a label

    Args:
        project_name (str):
        label_name (str):
        json_body (LabelUpdate):

    Returns:
        Response[Label]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        label_name=label_name,
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
    label_name: str,
    *,
    client: Client,
    json_body: LabelUpdate,
) -> Optional[Label]:
    """Update a label

    Args:
        project_name (str):
        label_name (str):
        json_body (LabelUpdate):

    Returns:
        Response[Label]
    """

    return sync_detailed(
        project_name=project_name,
        label_name=label_name,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    label_name: str,
    *,
    client: Client,
    json_body: LabelUpdate,
) -> Response[Label]:
    """Update a label

    Args:
        project_name (str):
        label_name (str):
        json_body (LabelUpdate):

    Returns:
        Response[Label]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        label_name=label_name,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    project_name: str,
    label_name: str,
    *,
    client: Client,
    json_body: LabelUpdate,
) -> Optional[Label]:
    """Update a label

    Args:
        project_name (str):
        label_name (str):
        json_body (LabelUpdate):

    Returns:
        Response[Label]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            label_name=label_name,
            client=client,
            json_body=json_body,
        )
    ).parsed
