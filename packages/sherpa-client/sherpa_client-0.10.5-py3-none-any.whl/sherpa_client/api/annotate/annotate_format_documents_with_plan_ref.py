from io import BytesIO
from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.input_document import InputDocument
from ...types import UNSET, File, Response, Unset


def _get_kwargs(
    project_name: str,
    plan_name: str,
    *,
    client: Client,
    json_body: List[InputDocument],
    inline_labels: Union[Unset, None, bool] = True,
    inline_label_ids: Union[Unset, None, bool] = True,
    inline_text: Union[Unset, None, bool] = True,
    debug: Union[Unset, None, bool] = False,
    parallelize: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/plans/{planName}/_annotate_format_documents".format(
        client.base_url, projectName=project_name, planName=plan_name
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["inlineLabels"] = inline_labels

    params["inlineLabelIds"] = inline_label_ids

    params["inlineText"] = inline_text

    params["debug"] = debug

    params["parallelize"] = parallelize

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = []
    for componentsschemas_input_document_array_item_data in json_body:
        componentsschemas_input_document_array_item = componentsschemas_input_document_array_item_data.to_dict()

        json_json_body.append(componentsschemas_input_document_array_item)

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[File]:
    if response.status_code == 200:
        response_200 = File(payload=BytesIO(response.json()))

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[File]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    project_name: str,
    plan_name: str,
    *,
    client: Client,
    json_body: List[InputDocument],
    inline_labels: Union[Unset, None, bool] = True,
    inline_label_ids: Union[Unset, None, bool] = True,
    inline_text: Union[Unset, None, bool] = True,
    debug: Union[Unset, None, bool] = False,
    parallelize: Union[Unset, None, bool] = False,
) -> Response[File]:
    """annotate documents with multiple annotators and return formatted results in a zip

    Args:
        project_name (str):
        plan_name (str):
        inline_labels (Union[Unset, None, bool]):  Default: True.
        inline_label_ids (Union[Unset, None, bool]):  Default: True.
        inline_text (Union[Unset, None, bool]):  Default: True.
        debug (Union[Unset, None, bool]):
        parallelize (Union[Unset, None, bool]):
        json_body (List[InputDocument]):

    Returns:
        Response[File]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        plan_name=plan_name,
        client=client,
        json_body=json_body,
        inline_labels=inline_labels,
        inline_label_ids=inline_label_ids,
        inline_text=inline_text,
        debug=debug,
        parallelize=parallelize,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    project_name: str,
    plan_name: str,
    *,
    client: Client,
    json_body: List[InputDocument],
    inline_labels: Union[Unset, None, bool] = True,
    inline_label_ids: Union[Unset, None, bool] = True,
    inline_text: Union[Unset, None, bool] = True,
    debug: Union[Unset, None, bool] = False,
    parallelize: Union[Unset, None, bool] = False,
) -> Optional[File]:
    """annotate documents with multiple annotators and return formatted results in a zip

    Args:
        project_name (str):
        plan_name (str):
        inline_labels (Union[Unset, None, bool]):  Default: True.
        inline_label_ids (Union[Unset, None, bool]):  Default: True.
        inline_text (Union[Unset, None, bool]):  Default: True.
        debug (Union[Unset, None, bool]):
        parallelize (Union[Unset, None, bool]):
        json_body (List[InputDocument]):

    Returns:
        Response[File]
    """

    return sync_detailed(
        project_name=project_name,
        plan_name=plan_name,
        client=client,
        json_body=json_body,
        inline_labels=inline_labels,
        inline_label_ids=inline_label_ids,
        inline_text=inline_text,
        debug=debug,
        parallelize=parallelize,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    plan_name: str,
    *,
    client: Client,
    json_body: List[InputDocument],
    inline_labels: Union[Unset, None, bool] = True,
    inline_label_ids: Union[Unset, None, bool] = True,
    inline_text: Union[Unset, None, bool] = True,
    debug: Union[Unset, None, bool] = False,
    parallelize: Union[Unset, None, bool] = False,
) -> Response[File]:
    """annotate documents with multiple annotators and return formatted results in a zip

    Args:
        project_name (str):
        plan_name (str):
        inline_labels (Union[Unset, None, bool]):  Default: True.
        inline_label_ids (Union[Unset, None, bool]):  Default: True.
        inline_text (Union[Unset, None, bool]):  Default: True.
        debug (Union[Unset, None, bool]):
        parallelize (Union[Unset, None, bool]):
        json_body (List[InputDocument]):

    Returns:
        Response[File]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        plan_name=plan_name,
        client=client,
        json_body=json_body,
        inline_labels=inline_labels,
        inline_label_ids=inline_label_ids,
        inline_text=inline_text,
        debug=debug,
        parallelize=parallelize,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    project_name: str,
    plan_name: str,
    *,
    client: Client,
    json_body: List[InputDocument],
    inline_labels: Union[Unset, None, bool] = True,
    inline_label_ids: Union[Unset, None, bool] = True,
    inline_text: Union[Unset, None, bool] = True,
    debug: Union[Unset, None, bool] = False,
    parallelize: Union[Unset, None, bool] = False,
) -> Optional[File]:
    """annotate documents with multiple annotators and return formatted results in a zip

    Args:
        project_name (str):
        plan_name (str):
        inline_labels (Union[Unset, None, bool]):  Default: True.
        inline_label_ids (Union[Unset, None, bool]):  Default: True.
        inline_text (Union[Unset, None, bool]):  Default: True.
        debug (Union[Unset, None, bool]):
        parallelize (Union[Unset, None, bool]):
        json_body (List[InputDocument]):

    Returns:
        Response[File]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            plan_name=plan_name,
            client=client,
            json_body=json_body,
            inline_labels=inline_labels,
            inline_label_ids=inline_label_ids,
            inline_text=inline_text,
            debug=debug,
            parallelize=parallelize,
        )
    ).parsed
