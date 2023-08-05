from typing import Any, Dict

import httpx

from ...client import Client
from ...models.share_mode import ShareMode
from ...types import UNSET, Response


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
    json_body: ShareMode,
    username: str,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/shares/users".format(client.base_url, projectName=project_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["username"] = username

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    project_name: str,
    *,
    client: Client,
    json_body: ShareMode,
    username: str,
) -> Response[Any]:
    """
    Args:
        project_name (str):
        username (str):
        json_body (ShareMode):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        json_body=json_body,
        username=username,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    project_name: str,
    *,
    client: Client,
    json_body: ShareMode,
    username: str,
) -> Response[Any]:
    """
    Args:
        project_name (str):
        username (str):
        json_body (ShareMode):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        json_body=json_body,
        username=username,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
