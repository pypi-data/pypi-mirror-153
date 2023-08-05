from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.document_hits import DocumentHits
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
    query: Union[Unset, None, str] = "",
    from_: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 10,
    highlight: Union[Unset, None, bool] = False,
    facet: Union[Unset, None, bool] = False,
    query_filter: Union[Unset, None, str] = "",
    output_fields: Union[Unset, None, str] = "",
    simple_query: Union[Unset, None, bool] = False,
    selected_facets: Union[Unset, None, List[str]] = UNSET,
    html_version: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/documents/_search".format(client.base_url, projectName=project_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["query"] = query

    params["from"] = from_

    params["size"] = size

    params["highlight"] = highlight

    params["facet"] = facet

    params["queryFilter"] = query_filter

    params["outputFields"] = output_fields

    params["simpleQuery"] = simple_query

    json_selected_facets: Union[Unset, None, List[str]] = UNSET
    if not isinstance(selected_facets, Unset):
        if selected_facets is None:
            json_selected_facets = None
        else:
            json_selected_facets = selected_facets

    params["selectedFacets"] = json_selected_facets

    params["htmlVersion"] = html_version

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[DocumentHits]:
    if response.status_code == 200:
        response_200 = DocumentHits.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[DocumentHits]:
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
    from_: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 10,
    highlight: Union[Unset, None, bool] = False,
    facet: Union[Unset, None, bool] = False,
    query_filter: Union[Unset, None, str] = "",
    output_fields: Union[Unset, None, str] = "",
    simple_query: Union[Unset, None, bool] = False,
    selected_facets: Union[Unset, None, List[str]] = UNSET,
    html_version: Union[Unset, None, bool] = False,
) -> Response[DocumentHits]:
    """Search for documents

    Args:
        project_name (str):
        query (Union[Unset, None, str]):  Default: ''.
        from_ (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 10.
        highlight (Union[Unset, None, bool]):
        facet (Union[Unset, None, bool]):
        query_filter (Union[Unset, None, str]):  Default: ''.
        output_fields (Union[Unset, None, str]):  Default: ''.
        simple_query (Union[Unset, None, bool]):
        selected_facets (Union[Unset, None, List[str]]):
        html_version (Union[Unset, None, bool]):

    Returns:
        Response[DocumentHits]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        query=query,
        from_=from_,
        size=size,
        highlight=highlight,
        facet=facet,
        query_filter=query_filter,
        output_fields=output_fields,
        simple_query=simple_query,
        selected_facets=selected_facets,
        html_version=html_version,
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
    from_: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 10,
    highlight: Union[Unset, None, bool] = False,
    facet: Union[Unset, None, bool] = False,
    query_filter: Union[Unset, None, str] = "",
    output_fields: Union[Unset, None, str] = "",
    simple_query: Union[Unset, None, bool] = False,
    selected_facets: Union[Unset, None, List[str]] = UNSET,
    html_version: Union[Unset, None, bool] = False,
) -> Optional[DocumentHits]:
    """Search for documents

    Args:
        project_name (str):
        query (Union[Unset, None, str]):  Default: ''.
        from_ (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 10.
        highlight (Union[Unset, None, bool]):
        facet (Union[Unset, None, bool]):
        query_filter (Union[Unset, None, str]):  Default: ''.
        output_fields (Union[Unset, None, str]):  Default: ''.
        simple_query (Union[Unset, None, bool]):
        selected_facets (Union[Unset, None, List[str]]):
        html_version (Union[Unset, None, bool]):

    Returns:
        Response[DocumentHits]
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        query=query,
        from_=from_,
        size=size,
        highlight=highlight,
        facet=facet,
        query_filter=query_filter,
        output_fields=output_fields,
        simple_query=simple_query,
        selected_facets=selected_facets,
        html_version=html_version,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Client,
    query: Union[Unset, None, str] = "",
    from_: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 10,
    highlight: Union[Unset, None, bool] = False,
    facet: Union[Unset, None, bool] = False,
    query_filter: Union[Unset, None, str] = "",
    output_fields: Union[Unset, None, str] = "",
    simple_query: Union[Unset, None, bool] = False,
    selected_facets: Union[Unset, None, List[str]] = UNSET,
    html_version: Union[Unset, None, bool] = False,
) -> Response[DocumentHits]:
    """Search for documents

    Args:
        project_name (str):
        query (Union[Unset, None, str]):  Default: ''.
        from_ (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 10.
        highlight (Union[Unset, None, bool]):
        facet (Union[Unset, None, bool]):
        query_filter (Union[Unset, None, str]):  Default: ''.
        output_fields (Union[Unset, None, str]):  Default: ''.
        simple_query (Union[Unset, None, bool]):
        selected_facets (Union[Unset, None, List[str]]):
        html_version (Union[Unset, None, bool]):

    Returns:
        Response[DocumentHits]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        query=query,
        from_=from_,
        size=size,
        highlight=highlight,
        facet=facet,
        query_filter=query_filter,
        output_fields=output_fields,
        simple_query=simple_query,
        selected_facets=selected_facets,
        html_version=html_version,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    project_name: str,
    *,
    client: Client,
    query: Union[Unset, None, str] = "",
    from_: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 10,
    highlight: Union[Unset, None, bool] = False,
    facet: Union[Unset, None, bool] = False,
    query_filter: Union[Unset, None, str] = "",
    output_fields: Union[Unset, None, str] = "",
    simple_query: Union[Unset, None, bool] = False,
    selected_facets: Union[Unset, None, List[str]] = UNSET,
    html_version: Union[Unset, None, bool] = False,
) -> Optional[DocumentHits]:
    """Search for documents

    Args:
        project_name (str):
        query (Union[Unset, None, str]):  Default: ''.
        from_ (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 10.
        highlight (Union[Unset, None, bool]):
        facet (Union[Unset, None, bool]):
        query_filter (Union[Unset, None, str]):  Default: ''.
        output_fields (Union[Unset, None, str]):  Default: ''.
        simple_query (Union[Unset, None, bool]):
        selected_facets (Union[Unset, None, List[str]]):
        html_version (Union[Unset, None, bool]):

    Returns:
        Response[DocumentHits]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            query=query,
            from_=from_,
            size=size,
            highlight=highlight,
            facet=facet,
            query_filter=query_filter,
            output_fields=output_fields,
            simple_query=simple_query,
            selected_facets=selected_facets,
            html_version=html_version,
        )
    ).parsed
