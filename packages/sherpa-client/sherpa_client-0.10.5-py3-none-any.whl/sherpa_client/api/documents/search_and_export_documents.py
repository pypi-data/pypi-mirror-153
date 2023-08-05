from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.document import Document
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
    query: Union[Unset, None, str] = "",
    query_filter: Union[Unset, None, str] = "",
    simple_query: Union[Unset, None, bool] = False,
    output_fields: Union[Unset, None, str] = "",
    selected_facets: Union[Unset, None, List[str]] = UNSET,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/documents/_search_and_export".format(client.base_url, projectName=project_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["query"] = query

    params["queryFilter"] = query_filter

    params["simpleQuery"] = simple_query

    params["outputFields"] = output_fields

    json_selected_facets: Union[Unset, None, List[str]] = UNSET
    if not isinstance(selected_facets, Unset):
        if selected_facets is None:
            json_selected_facets = None
        else:
            json_selected_facets = selected_facets

    params["selectedFacets"] = json_selected_facets

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
    query: Union[Unset, None, str] = "",
    query_filter: Union[Unset, None, str] = "",
    simple_query: Union[Unset, None, bool] = False,
    output_fields: Union[Unset, None, str] = "",
    selected_facets: Union[Unset, None, List[str]] = UNSET,
) -> Response[List[Document]]:
    """Search for documents and export them

    Args:
        project_name (str):
        query (Union[Unset, None, str]):  Default: ''.
        query_filter (Union[Unset, None, str]):  Default: ''.
        simple_query (Union[Unset, None, bool]):
        output_fields (Union[Unset, None, str]):  Default: ''.
        selected_facets (Union[Unset, None, List[str]]):

    Returns:
        Response[List[Document]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        query=query,
        query_filter=query_filter,
        simple_query=simple_query,
        output_fields=output_fields,
        selected_facets=selected_facets,
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
    query: Union[Unset, None, str] = "",
    query_filter: Union[Unset, None, str] = "",
    simple_query: Union[Unset, None, bool] = False,
    output_fields: Union[Unset, None, str] = "",
    selected_facets: Union[Unset, None, List[str]] = UNSET,
) -> Optional[List[Document]]:
    """Search for documents and export them

    Args:
        project_name (str):
        query (Union[Unset, None, str]):  Default: ''.
        query_filter (Union[Unset, None, str]):  Default: ''.
        simple_query (Union[Unset, None, bool]):
        output_fields (Union[Unset, None, str]):  Default: ''.
        selected_facets (Union[Unset, None, List[str]]):

    Returns:
        Response[List[Document]]
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        query=query,
        query_filter=query_filter,
        simple_query=simple_query,
        output_fields=output_fields,
        selected_facets=selected_facets,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Client,
    query: Union[Unset, None, str] = "",
    query_filter: Union[Unset, None, str] = "",
    simple_query: Union[Unset, None, bool] = False,
    output_fields: Union[Unset, None, str] = "",
    selected_facets: Union[Unset, None, List[str]] = UNSET,
) -> Response[List[Document]]:
    """Search for documents and export them

    Args:
        project_name (str):
        query (Union[Unset, None, str]):  Default: ''.
        query_filter (Union[Unset, None, str]):  Default: ''.
        simple_query (Union[Unset, None, bool]):
        output_fields (Union[Unset, None, str]):  Default: ''.
        selected_facets (Union[Unset, None, List[str]]):

    Returns:
        Response[List[Document]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        query=query,
        query_filter=query_filter,
        simple_query=simple_query,
        output_fields=output_fields,
        selected_facets=selected_facets,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    project_name: str,
    *,
    client: Client,
    query: Union[Unset, None, str] = "",
    query_filter: Union[Unset, None, str] = "",
    simple_query: Union[Unset, None, bool] = False,
    output_fields: Union[Unset, None, str] = "",
    selected_facets: Union[Unset, None, List[str]] = UNSET,
) -> Optional[List[Document]]:
    """Search for documents and export them

    Args:
        project_name (str):
        query (Union[Unset, None, str]):  Default: ''.
        query_filter (Union[Unset, None, str]):  Default: ''.
        simple_query (Union[Unset, None, bool]):
        output_fields (Union[Unset, None, str]):  Default: ''.
        selected_facets (Union[Unset, None, List[str]]):

    Returns:
        Response[List[Document]]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            query=query,
            query_filter=query_filter,
            simple_query=simple_query,
            output_fields=output_fields,
            selected_facets=selected_facets,
        )
    ).parsed
