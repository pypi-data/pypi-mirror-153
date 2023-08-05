from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.generated_label_hint import GeneratedLabelHint
from ...models.input_label import InputLabel
from ...types import Response


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
    json_body: InputLabel,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/suggesters/_label_hint".format(client.base_url, projectName=project_name)

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


def _parse_response(*, response: httpx.Response) -> Optional[GeneratedLabelHint]:
    if response.status_code == 200:
        response_200 = GeneratedLabelHint.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[GeneratedLabelHint]:
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
    json_body: InputLabel,
) -> Response[GeneratedLabelHint]:
    """Get a somehow unique suggester label generated after the provided suggester label

    Args:
        project_name (str):
        json_body (InputLabel):

    Returns:
        Response[GeneratedLabelHint]
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
    json_body: InputLabel,
) -> Optional[GeneratedLabelHint]:
    """Get a somehow unique suggester label generated after the provided suggester label

    Args:
        project_name (str):
        json_body (InputLabel):

    Returns:
        Response[GeneratedLabelHint]
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
    json_body: InputLabel,
) -> Response[GeneratedLabelHint]:
    """Get a somehow unique suggester label generated after the provided suggester label

    Args:
        project_name (str):
        json_body (InputLabel):

    Returns:
        Response[GeneratedLabelHint]
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
    json_body: InputLabel,
) -> Optional[GeneratedLabelHint]:
    """Get a somehow unique suggester label generated after the provided suggester label

    Args:
        project_name (str):
        json_body (InputLabel):

    Returns:
        Response[GeneratedLabelHint]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            json_body=json_body,
        )
    ).parsed
