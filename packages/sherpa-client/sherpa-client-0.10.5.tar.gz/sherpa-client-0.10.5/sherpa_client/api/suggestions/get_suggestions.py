from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.get_suggestions_response_200 import GetSuggestionsResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
    from_: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 25,
    sort: Union[Unset, None, str] = "sampling",
    filter_: Union[Unset, None, str] = "",
    html_version: Union[Unset, None, bool] = False,
    facet: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/suggestions".format(client.base_url, projectName=project_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["from"] = from_

    params["size"] = size

    params["sort"] = sort

    params["filter"] = filter_

    params["htmlVersion"] = html_version

    params["facet"] = facet

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[GetSuggestionsResponse200]:
    if response.status_code == 200:
        response_200 = GetSuggestionsResponse200.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[GetSuggestionsResponse200]:
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
    from_: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 25,
    sort: Union[Unset, None, str] = "sampling",
    filter_: Union[Unset, None, str] = "",
    html_version: Union[Unset, None, bool] = False,
    facet: Union[Unset, None, bool] = False,
) -> Response[GetSuggestionsResponse200]:
    """Get suggestions according to the project nature

    Args:
        project_name (str):
        from_ (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 25.
        sort (Union[Unset, None, str]):  Default: 'sampling'.
        filter_ (Union[Unset, None, str]):  Default: ''.
        html_version (Union[Unset, None, bool]):
        facet (Union[Unset, None, bool]):

    Returns:
        Response[GetSuggestionsResponse200]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        from_=from_,
        size=size,
        sort=sort,
        filter_=filter_,
        html_version=html_version,
        facet=facet,
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
    from_: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 25,
    sort: Union[Unset, None, str] = "sampling",
    filter_: Union[Unset, None, str] = "",
    html_version: Union[Unset, None, bool] = False,
    facet: Union[Unset, None, bool] = False,
) -> Optional[GetSuggestionsResponse200]:
    """Get suggestions according to the project nature

    Args:
        project_name (str):
        from_ (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 25.
        sort (Union[Unset, None, str]):  Default: 'sampling'.
        filter_ (Union[Unset, None, str]):  Default: ''.
        html_version (Union[Unset, None, bool]):
        facet (Union[Unset, None, bool]):

    Returns:
        Response[GetSuggestionsResponse200]
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        from_=from_,
        size=size,
        sort=sort,
        filter_=filter_,
        html_version=html_version,
        facet=facet,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Client,
    from_: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 25,
    sort: Union[Unset, None, str] = "sampling",
    filter_: Union[Unset, None, str] = "",
    html_version: Union[Unset, None, bool] = False,
    facet: Union[Unset, None, bool] = False,
) -> Response[GetSuggestionsResponse200]:
    """Get suggestions according to the project nature

    Args:
        project_name (str):
        from_ (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 25.
        sort (Union[Unset, None, str]):  Default: 'sampling'.
        filter_ (Union[Unset, None, str]):  Default: ''.
        html_version (Union[Unset, None, bool]):
        facet (Union[Unset, None, bool]):

    Returns:
        Response[GetSuggestionsResponse200]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        from_=from_,
        size=size,
        sort=sort,
        filter_=filter_,
        html_version=html_version,
        facet=facet,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    project_name: str,
    *,
    client: Client,
    from_: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 25,
    sort: Union[Unset, None, str] = "sampling",
    filter_: Union[Unset, None, str] = "",
    html_version: Union[Unset, None, bool] = False,
    facet: Union[Unset, None, bool] = False,
) -> Optional[GetSuggestionsResponse200]:
    """Get suggestions according to the project nature

    Args:
        project_name (str):
        from_ (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 25.
        sort (Union[Unset, None, str]):  Default: 'sampling'.
        filter_ (Union[Unset, None, str]):  Default: ''.
        html_version (Union[Unset, None, bool]):
        facet (Union[Unset, None, bool]):

    Returns:
        Response[GetSuggestionsResponse200]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            from_=from_,
            size=size,
            sort=sort,
            filter_=filter_,
            html_version=html_version,
            facet=facet,
        )
    ).parsed
