from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.http_service_record import HttpServiceRecord
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    name: Union[Unset, None, str] = "",
    api: Union[Unset, None, str] = "",
    engine: Union[Unset, None, str] = "",
    function: Union[Unset, None, str] = "",
    language: Union[Unset, None, str] = "",
    type: Union[Unset, None, str] = "",
    nature: Union[Unset, None, str] = "",
    version: Union[Unset, None, str] = "",
    term_importer: Union[Unset, None, str] = "",
    annotator: Union[Unset, None, str] = "",
    processor: Union[Unset, None, str] = "",
    formatter: Union[Unset, None, str] = "",
    converter: Union[Unset, None, str] = "",
) -> Dict[str, Any]:
    url = "{}/services".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["name"] = name

    params["api"] = api

    params["engine"] = engine

    params["function"] = function

    params["language"] = language

    params["type"] = type

    params["nature"] = nature

    params["version"] = version

    params["termImporter"] = term_importer

    params["annotator"] = annotator

    params["processor"] = processor

    params["formatter"] = formatter

    params["converter"] = converter

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[List[HttpServiceRecord]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_http_service_record_array_item_data in _response_200:
            componentsschemas_http_service_record_array_item = HttpServiceRecord.from_dict(
                componentsschemas_http_service_record_array_item_data
            )

            response_200.append(componentsschemas_http_service_record_array_item)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[List[HttpServiceRecord]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    name: Union[Unset, None, str] = "",
    api: Union[Unset, None, str] = "",
    engine: Union[Unset, None, str] = "",
    function: Union[Unset, None, str] = "",
    language: Union[Unset, None, str] = "",
    type: Union[Unset, None, str] = "",
    nature: Union[Unset, None, str] = "",
    version: Union[Unset, None, str] = "",
    term_importer: Union[Unset, None, str] = "",
    annotator: Union[Unset, None, str] = "",
    processor: Union[Unset, None, str] = "",
    formatter: Union[Unset, None, str] = "",
    converter: Union[Unset, None, str] = "",
) -> Response[List[HttpServiceRecord]]:
    """Filter the list of available services

    Args:
        name (Union[Unset, None, str]):  Default: ''.
        api (Union[Unset, None, str]):  Default: ''.
        engine (Union[Unset, None, str]):  Default: ''.
        function (Union[Unset, None, str]):  Default: ''.
        language (Union[Unset, None, str]):  Default: ''.
        type (Union[Unset, None, str]):  Default: ''.
        nature (Union[Unset, None, str]):  Default: ''.
        version (Union[Unset, None, str]):  Default: ''.
        term_importer (Union[Unset, None, str]):  Default: ''.
        annotator (Union[Unset, None, str]):  Default: ''.
        processor (Union[Unset, None, str]):  Default: ''.
        formatter (Union[Unset, None, str]):  Default: ''.
        converter (Union[Unset, None, str]):  Default: ''.

    Returns:
        Response[List[HttpServiceRecord]]
    """

    kwargs = _get_kwargs(
        client=client,
        name=name,
        api=api,
        engine=engine,
        function=function,
        language=language,
        type=type,
        nature=nature,
        version=version,
        term_importer=term_importer,
        annotator=annotator,
        processor=processor,
        formatter=formatter,
        converter=converter,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    name: Union[Unset, None, str] = "",
    api: Union[Unset, None, str] = "",
    engine: Union[Unset, None, str] = "",
    function: Union[Unset, None, str] = "",
    language: Union[Unset, None, str] = "",
    type: Union[Unset, None, str] = "",
    nature: Union[Unset, None, str] = "",
    version: Union[Unset, None, str] = "",
    term_importer: Union[Unset, None, str] = "",
    annotator: Union[Unset, None, str] = "",
    processor: Union[Unset, None, str] = "",
    formatter: Union[Unset, None, str] = "",
    converter: Union[Unset, None, str] = "",
) -> Optional[List[HttpServiceRecord]]:
    """Filter the list of available services

    Args:
        name (Union[Unset, None, str]):  Default: ''.
        api (Union[Unset, None, str]):  Default: ''.
        engine (Union[Unset, None, str]):  Default: ''.
        function (Union[Unset, None, str]):  Default: ''.
        language (Union[Unset, None, str]):  Default: ''.
        type (Union[Unset, None, str]):  Default: ''.
        nature (Union[Unset, None, str]):  Default: ''.
        version (Union[Unset, None, str]):  Default: ''.
        term_importer (Union[Unset, None, str]):  Default: ''.
        annotator (Union[Unset, None, str]):  Default: ''.
        processor (Union[Unset, None, str]):  Default: ''.
        formatter (Union[Unset, None, str]):  Default: ''.
        converter (Union[Unset, None, str]):  Default: ''.

    Returns:
        Response[List[HttpServiceRecord]]
    """

    return sync_detailed(
        client=client,
        name=name,
        api=api,
        engine=engine,
        function=function,
        language=language,
        type=type,
        nature=nature,
        version=version,
        term_importer=term_importer,
        annotator=annotator,
        processor=processor,
        formatter=formatter,
        converter=converter,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    name: Union[Unset, None, str] = "",
    api: Union[Unset, None, str] = "",
    engine: Union[Unset, None, str] = "",
    function: Union[Unset, None, str] = "",
    language: Union[Unset, None, str] = "",
    type: Union[Unset, None, str] = "",
    nature: Union[Unset, None, str] = "",
    version: Union[Unset, None, str] = "",
    term_importer: Union[Unset, None, str] = "",
    annotator: Union[Unset, None, str] = "",
    processor: Union[Unset, None, str] = "",
    formatter: Union[Unset, None, str] = "",
    converter: Union[Unset, None, str] = "",
) -> Response[List[HttpServiceRecord]]:
    """Filter the list of available services

    Args:
        name (Union[Unset, None, str]):  Default: ''.
        api (Union[Unset, None, str]):  Default: ''.
        engine (Union[Unset, None, str]):  Default: ''.
        function (Union[Unset, None, str]):  Default: ''.
        language (Union[Unset, None, str]):  Default: ''.
        type (Union[Unset, None, str]):  Default: ''.
        nature (Union[Unset, None, str]):  Default: ''.
        version (Union[Unset, None, str]):  Default: ''.
        term_importer (Union[Unset, None, str]):  Default: ''.
        annotator (Union[Unset, None, str]):  Default: ''.
        processor (Union[Unset, None, str]):  Default: ''.
        formatter (Union[Unset, None, str]):  Default: ''.
        converter (Union[Unset, None, str]):  Default: ''.

    Returns:
        Response[List[HttpServiceRecord]]
    """

    kwargs = _get_kwargs(
        client=client,
        name=name,
        api=api,
        engine=engine,
        function=function,
        language=language,
        type=type,
        nature=nature,
        version=version,
        term_importer=term_importer,
        annotator=annotator,
        processor=processor,
        formatter=formatter,
        converter=converter,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    name: Union[Unset, None, str] = "",
    api: Union[Unset, None, str] = "",
    engine: Union[Unset, None, str] = "",
    function: Union[Unset, None, str] = "",
    language: Union[Unset, None, str] = "",
    type: Union[Unset, None, str] = "",
    nature: Union[Unset, None, str] = "",
    version: Union[Unset, None, str] = "",
    term_importer: Union[Unset, None, str] = "",
    annotator: Union[Unset, None, str] = "",
    processor: Union[Unset, None, str] = "",
    formatter: Union[Unset, None, str] = "",
    converter: Union[Unset, None, str] = "",
) -> Optional[List[HttpServiceRecord]]:
    """Filter the list of available services

    Args:
        name (Union[Unset, None, str]):  Default: ''.
        api (Union[Unset, None, str]):  Default: ''.
        engine (Union[Unset, None, str]):  Default: ''.
        function (Union[Unset, None, str]):  Default: ''.
        language (Union[Unset, None, str]):  Default: ''.
        type (Union[Unset, None, str]):  Default: ''.
        nature (Union[Unset, None, str]):  Default: ''.
        version (Union[Unset, None, str]):  Default: ''.
        term_importer (Union[Unset, None, str]):  Default: ''.
        annotator (Union[Unset, None, str]):  Default: ''.
        processor (Union[Unset, None, str]):  Default: ''.
        formatter (Union[Unset, None, str]):  Default: ''.
        converter (Union[Unset, None, str]):  Default: ''.

    Returns:
        Response[List[HttpServiceRecord]]
    """

    return (
        await asyncio_detailed(
            client=client,
            name=name,
            api=api,
            engine=engine,
            function=function,
            language=language,
            type=type,
            nature=nature,
            version=version,
            term_importer=term_importer,
            annotator=annotator,
            processor=processor,
            formatter=formatter,
            converter=converter,
        )
    ).parsed
