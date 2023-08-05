from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.document import Document
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
    sample_size: Union[Unset, None, int] = 25,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/documents/_sample".format(client.base_url, projectName=project_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["sampleSize"] = sample_size

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[List[Document]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_document_array_item_data in _response_200:
            componentsschemas_document_array_item = Document.from_dict(componentsschemas_document_array_item_data)

            response_200.append(componentsschemas_document_array_item)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[List[Document]]:
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
    sample_size: Union[Unset, None, int] = 25,
) -> Response[List[Document]]:
    """Get a sample of documents in dataset

    Args:
        project_name (str):
        sample_size (Union[Unset, None, int]):  Default: 25.

    Returns:
        Response[List[Document]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        sample_size=sample_size,
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
    sample_size: Union[Unset, None, int] = 25,
) -> Optional[List[Document]]:
    """Get a sample of documents in dataset

    Args:
        project_name (str):
        sample_size (Union[Unset, None, int]):  Default: 25.

    Returns:
        Response[List[Document]]
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        sample_size=sample_size,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Client,
    sample_size: Union[Unset, None, int] = 25,
) -> Response[List[Document]]:
    """Get a sample of documents in dataset

    Args:
        project_name (str):
        sample_size (Union[Unset, None, int]):  Default: 25.

    Returns:
        Response[List[Document]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        sample_size=sample_size,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    project_name: str,
    *,
    client: Client,
    sample_size: Union[Unset, None, int] = 25,
) -> Optional[List[Document]]:
    """Get a sample of documents in dataset

    Args:
        project_name (str):
        sample_size (Union[Unset, None, int]):  Default: 25.

    Returns:
        Response[List[Document]]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            sample_size=sample_size,
        )
    ).parsed
