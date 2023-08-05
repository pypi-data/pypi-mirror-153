from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.document import Document
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    doc_id: str,
    *,
    client: Client,
    output_fields: Union[Unset, None, str] = UNSET,
    html_version: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/documents/{docId}".format(client.base_url, projectName=project_name, docId=doc_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["outputFields"] = output_fields

    params["htmlVersion"] = html_version

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, Document]]:
    if response.status_code == 200:
        response_200 = Document.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, Document]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    project_name: str,
    doc_id: str,
    *,
    client: Client,
    output_fields: Union[Unset, None, str] = UNSET,
    html_version: Union[Unset, None, bool] = False,
) -> Response[Union[Any, Document]]:
    """Get a specific document

    Args:
        project_name (str):
        doc_id (str):
        output_fields (Union[Unset, None, str]):
        html_version (Union[Unset, None, bool]):

    Returns:
        Response[Union[Any, Document]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        doc_id=doc_id,
        client=client,
        output_fields=output_fields,
        html_version=html_version,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    project_name: str,
    doc_id: str,
    *,
    client: Client,
    output_fields: Union[Unset, None, str] = UNSET,
    html_version: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, Document]]:
    """Get a specific document

    Args:
        project_name (str):
        doc_id (str):
        output_fields (Union[Unset, None, str]):
        html_version (Union[Unset, None, bool]):

    Returns:
        Response[Union[Any, Document]]
    """

    return sync_detailed(
        project_name=project_name,
        doc_id=doc_id,
        client=client,
        output_fields=output_fields,
        html_version=html_version,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    doc_id: str,
    *,
    client: Client,
    output_fields: Union[Unset, None, str] = UNSET,
    html_version: Union[Unset, None, bool] = False,
) -> Response[Union[Any, Document]]:
    """Get a specific document

    Args:
        project_name (str):
        doc_id (str):
        output_fields (Union[Unset, None, str]):
        html_version (Union[Unset, None, bool]):

    Returns:
        Response[Union[Any, Document]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        doc_id=doc_id,
        client=client,
        output_fields=output_fields,
        html_version=html_version,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    project_name: str,
    doc_id: str,
    *,
    client: Client,
    output_fields: Union[Unset, None, str] = UNSET,
    html_version: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, Document]]:
    """Get a specific document

    Args:
        project_name (str):
        doc_id (str):
        output_fields (Union[Unset, None, str]):
        html_version (Union[Unset, None, bool]):

    Returns:
        Response[Union[Any, Document]]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            doc_id=doc_id,
            client=client,
            output_fields=output_fields,
            html_version=html_version,
        )
    ).parsed
