from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.operation_count import OperationCount
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
    labels: Union[Unset, None, List[str]] = UNSET,
    created_by: Union[Unset, None, List[str]] = UNSET,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/annotations/_clear".format(client.base_url, projectName=project_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_labels: Union[Unset, None, List[str]] = UNSET
    if not isinstance(labels, Unset):
        if labels is None:
            json_labels = None
        else:
            json_labels = labels

    params["labels"] = json_labels

    json_created_by: Union[Unset, None, List[str]] = UNSET
    if not isinstance(created_by, Unset):
        if created_by is None:
            json_created_by = None
        else:
            json_created_by = created_by

    params["createdBy"] = json_created_by

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[OperationCount]:
    if response.status_code == 200:
        response_200 = OperationCount.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[OperationCount]:
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
    labels: Union[Unset, None, List[str]] = UNSET,
    created_by: Union[Unset, None, List[str]] = UNSET,
) -> Response[OperationCount]:
    """Delete annotations from the corpus

    Args:
        project_name (str):
        labels (Union[Unset, None, List[str]]):
        created_by (Union[Unset, None, List[str]]):

    Returns:
        Response[OperationCount]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        labels=labels,
        created_by=created_by,
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
    labels: Union[Unset, None, List[str]] = UNSET,
    created_by: Union[Unset, None, List[str]] = UNSET,
) -> Optional[OperationCount]:
    """Delete annotations from the corpus

    Args:
        project_name (str):
        labels (Union[Unset, None, List[str]]):
        created_by (Union[Unset, None, List[str]]):

    Returns:
        Response[OperationCount]
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        labels=labels,
        created_by=created_by,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Client,
    labels: Union[Unset, None, List[str]] = UNSET,
    created_by: Union[Unset, None, List[str]] = UNSET,
) -> Response[OperationCount]:
    """Delete annotations from the corpus

    Args:
        project_name (str):
        labels (Union[Unset, None, List[str]]):
        created_by (Union[Unset, None, List[str]]):

    Returns:
        Response[OperationCount]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        labels=labels,
        created_by=created_by,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    project_name: str,
    *,
    client: Client,
    labels: Union[Unset, None, List[str]] = UNSET,
    created_by: Union[Unset, None, List[str]] = UNSET,
) -> Optional[OperationCount]:
    """Delete annotations from the corpus

    Args:
        project_name (str):
        labels (Union[Unset, None, List[str]]):
        created_by (Union[Unset, None, List[str]]):

    Returns:
        Response[OperationCount]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            labels=labels,
            created_by=created_by,
        )
    ).parsed
