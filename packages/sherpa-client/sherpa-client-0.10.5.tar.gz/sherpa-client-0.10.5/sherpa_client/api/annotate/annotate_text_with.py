from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.annotated_document import AnnotatedDocument
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    annotator: str,
    *,
    client: Client,
    text_body: str,
    inline_labels: Union[Unset, None, bool] = True,
    inline_label_ids: Union[Unset, None, bool] = True,
    inline_text: Union[Unset, None, bool] = True,
    debug: Union[Unset, None, bool] = False,
    parallelize: Union[Unset, None, bool] = False,
    output_fields: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/annotators/{annotator}/_annotate".format(
        client.base_url, projectName=project_name, annotator=annotator
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["inlineLabels"] = inline_labels

    params["inlineLabelIds"] = inline_label_ids

    params["inlineText"] = inline_text

    params["debug"] = debug

    params["parallelize"] = parallelize

    params["outputFields"] = output_fields

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    headers.update({"Content-Type": "text/plain"})

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "content": text_body,
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[AnnotatedDocument]:
    if response.status_code == 200:
        response_200 = AnnotatedDocument.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[AnnotatedDocument]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    project_name: str,
    annotator: str,
    *,
    client: Client,
    text_body: str,
    inline_labels: Union[Unset, None, bool] = True,
    inline_label_ids: Union[Unset, None, bool] = True,
    inline_text: Union[Unset, None, bool] = True,
    debug: Union[Unset, None, bool] = False,
    parallelize: Union[Unset, None, bool] = False,
    output_fields: Union[Unset, None, str] = UNSET,
) -> Response[AnnotatedDocument]:
    """Annotate text with the given annotator

    Args:
        project_name (str):
        annotator (str):
        inline_labels (Union[Unset, None, bool]):  Default: True.
        inline_label_ids (Union[Unset, None, bool]):  Default: True.
        inline_text (Union[Unset, None, bool]):  Default: True.
        debug (Union[Unset, None, bool]):
        parallelize (Union[Unset, None, bool]):
        output_fields (Union[Unset, None, str]):

    Returns:
        Response[AnnotatedDocument]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        annotator=annotator,
        client=client,
        text_body=text_body,
        inline_labels=inline_labels,
        inline_label_ids=inline_label_ids,
        inline_text=inline_text,
        debug=debug,
        parallelize=parallelize,
        output_fields=output_fields,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    project_name: str,
    annotator: str,
    *,
    client: Client,
    text_body: str,
    inline_labels: Union[Unset, None, bool] = True,
    inline_label_ids: Union[Unset, None, bool] = True,
    inline_text: Union[Unset, None, bool] = True,
    debug: Union[Unset, None, bool] = False,
    parallelize: Union[Unset, None, bool] = False,
    output_fields: Union[Unset, None, str] = UNSET,
) -> Optional[AnnotatedDocument]:
    """Annotate text with the given annotator

    Args:
        project_name (str):
        annotator (str):
        inline_labels (Union[Unset, None, bool]):  Default: True.
        inline_label_ids (Union[Unset, None, bool]):  Default: True.
        inline_text (Union[Unset, None, bool]):  Default: True.
        debug (Union[Unset, None, bool]):
        parallelize (Union[Unset, None, bool]):
        output_fields (Union[Unset, None, str]):

    Returns:
        Response[AnnotatedDocument]
    """

    return sync_detailed(
        project_name=project_name,
        annotator=annotator,
        client=client,
        text_body=text_body,
        inline_labels=inline_labels,
        inline_label_ids=inline_label_ids,
        inline_text=inline_text,
        debug=debug,
        parallelize=parallelize,
        output_fields=output_fields,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    annotator: str,
    *,
    client: Client,
    text_body: str,
    inline_labels: Union[Unset, None, bool] = True,
    inline_label_ids: Union[Unset, None, bool] = True,
    inline_text: Union[Unset, None, bool] = True,
    debug: Union[Unset, None, bool] = False,
    parallelize: Union[Unset, None, bool] = False,
    output_fields: Union[Unset, None, str] = UNSET,
) -> Response[AnnotatedDocument]:
    """Annotate text with the given annotator

    Args:
        project_name (str):
        annotator (str):
        inline_labels (Union[Unset, None, bool]):  Default: True.
        inline_label_ids (Union[Unset, None, bool]):  Default: True.
        inline_text (Union[Unset, None, bool]):  Default: True.
        debug (Union[Unset, None, bool]):
        parallelize (Union[Unset, None, bool]):
        output_fields (Union[Unset, None, str]):

    Returns:
        Response[AnnotatedDocument]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        annotator=annotator,
        client=client,
        text_body=text_body,
        inline_labels=inline_labels,
        inline_label_ids=inline_label_ids,
        inline_text=inline_text,
        debug=debug,
        parallelize=parallelize,
        output_fields=output_fields,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    project_name: str,
    annotator: str,
    *,
    client: Client,
    text_body: str,
    inline_labels: Union[Unset, None, bool] = True,
    inline_label_ids: Union[Unset, None, bool] = True,
    inline_text: Union[Unset, None, bool] = True,
    debug: Union[Unset, None, bool] = False,
    parallelize: Union[Unset, None, bool] = False,
    output_fields: Union[Unset, None, str] = UNSET,
) -> Optional[AnnotatedDocument]:
    """Annotate text with the given annotator

    Args:
        project_name (str):
        annotator (str):
        inline_labels (Union[Unset, None, bool]):  Default: True.
        inline_label_ids (Union[Unset, None, bool]):  Default: True.
        inline_text (Union[Unset, None, bool]):  Default: True.
        debug (Union[Unset, None, bool]):
        parallelize (Union[Unset, None, bool]):
        output_fields (Union[Unset, None, str]):

    Returns:
        Response[AnnotatedDocument]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            annotator=annotator,
            client=client,
            text_body=text_body,
            inline_labels=inline_labels,
            inline_label_ids=inline_label_ids,
            inline_text=inline_text,
            debug=debug,
            parallelize=parallelize,
            output_fields=output_fields,
        )
    ).parsed
