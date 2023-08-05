from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.lexicon import Lexicon
from ...types import Response


def _get_kwargs(
    project_name: str,
    lexicon_name: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/lexicons/{lexiconName}".format(
        client.base_url, projectName=project_name, lexiconName=lexicon_name
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "patch",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Lexicon]:
    if response.status_code == 200:
        response_200 = Lexicon.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Lexicon]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    project_name: str,
    lexicon_name: str,
    *,
    client: Client,
) -> Response[Lexicon]:
    """Update a lexicon

    Args:
        project_name (str):
        lexicon_name (str):

    Returns:
        Response[Lexicon]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        lexicon_name=lexicon_name,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    project_name: str,
    lexicon_name: str,
    *,
    client: Client,
) -> Optional[Lexicon]:
    """Update a lexicon

    Args:
        project_name (str):
        lexicon_name (str):

    Returns:
        Response[Lexicon]
    """

    return sync_detailed(
        project_name=project_name,
        lexicon_name=lexicon_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    lexicon_name: str,
    *,
    client: Client,
) -> Response[Lexicon]:
    """Update a lexicon

    Args:
        project_name (str):
        lexicon_name (str):

    Returns:
        Response[Lexicon]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        lexicon_name=lexicon_name,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    project_name: str,
    lexicon_name: str,
    *,
    client: Client,
) -> Optional[Lexicon]:
    """Update a lexicon

    Args:
        project_name (str):
        lexicon_name (str):

    Returns:
        Response[Lexicon]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            lexicon_name=lexicon_name,
            client=client,
        )
    ).parsed
