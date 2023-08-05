from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.get_project_engine_parameters_schema_response_200 import GetProjectEngineParametersSchemaResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
    type: str,
    engine: str,
    ui_schema: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/engine_parameters".format(client.base_url, projectName=project_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["type"] = type

    params["engine"] = engine

    params["uiSchema"] = ui_schema

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[GetProjectEngineParametersSchemaResponse200]:
    if response.status_code == 200:
        response_200 = GetProjectEngineParametersSchemaResponse200.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[GetProjectEngineParametersSchemaResponse200]:
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
    type: str,
    engine: str,
    ui_schema: Union[Unset, None, bool] = False,
) -> Response[GetProjectEngineParametersSchemaResponse200]:
    """Get the list of parameters of the given engine or engine function

    Args:
        project_name (str):
        type (str):
        engine (str):
        ui_schema (Union[Unset, None, bool]):

    Returns:
        Response[GetProjectEngineParametersSchemaResponse200]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        type=type,
        engine=engine,
        ui_schema=ui_schema,
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
    type: str,
    engine: str,
    ui_schema: Union[Unset, None, bool] = False,
) -> Optional[GetProjectEngineParametersSchemaResponse200]:
    """Get the list of parameters of the given engine or engine function

    Args:
        project_name (str):
        type (str):
        engine (str):
        ui_schema (Union[Unset, None, bool]):

    Returns:
        Response[GetProjectEngineParametersSchemaResponse200]
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        type=type,
        engine=engine,
        ui_schema=ui_schema,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Client,
    type: str,
    engine: str,
    ui_schema: Union[Unset, None, bool] = False,
) -> Response[GetProjectEngineParametersSchemaResponse200]:
    """Get the list of parameters of the given engine or engine function

    Args:
        project_name (str):
        type (str):
        engine (str):
        ui_schema (Union[Unset, None, bool]):

    Returns:
        Response[GetProjectEngineParametersSchemaResponse200]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        type=type,
        engine=engine,
        ui_schema=ui_schema,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    project_name: str,
    *,
    client: Client,
    type: str,
    engine: str,
    ui_schema: Union[Unset, None, bool] = False,
) -> Optional[GetProjectEngineParametersSchemaResponse200]:
    """Get the list of parameters of the given engine or engine function

    Args:
        project_name (str):
        type (str):
        engine (str):
        ui_schema (Union[Unset, None, bool]):

    Returns:
        Response[GetProjectEngineParametersSchemaResponse200]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            type=type,
            engine=engine,
            ui_schema=ui_schema,
        )
    ).parsed
