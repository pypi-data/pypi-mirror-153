from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.upload_files_multipart_data import UploadFilesMultipartData
from ...models.uploaded_file import UploadedFile
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    multipart_data: UploadFilesMultipartData,
    ttl: Union[Unset, None, int] = 0,
    image: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/uploads".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["ttl"] = ttl

    params["image"] = image

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    multipart_multipart_data = multipart_data.to_multipart()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "files": multipart_multipart_data,
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[List[UploadedFile]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_uploaded_file_array_item_data in _response_200:
            componentsschemas_uploaded_file_array_item = UploadedFile.from_dict(
                componentsschemas_uploaded_file_array_item_data
            )

            response_200.append(componentsschemas_uploaded_file_array_item)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[List[UploadedFile]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    multipart_data: UploadFilesMultipartData,
    ttl: Union[Unset, None, int] = 0,
    image: Union[Unset, None, bool] = False,
) -> Response[List[UploadedFile]]:
    """
    Args:
        ttl (Union[Unset, None, int]):
        image (Union[Unset, None, bool]):
        multipart_data (UploadFilesMultipartData):

    Returns:
        Response[List[UploadedFile]]
    """

    kwargs = _get_kwargs(
        client=client,
        multipart_data=multipart_data,
        ttl=ttl,
        image=image,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    multipart_data: UploadFilesMultipartData,
    ttl: Union[Unset, None, int] = 0,
    image: Union[Unset, None, bool] = False,
) -> Optional[List[UploadedFile]]:
    """
    Args:
        ttl (Union[Unset, None, int]):
        image (Union[Unset, None, bool]):
        multipart_data (UploadFilesMultipartData):

    Returns:
        Response[List[UploadedFile]]
    """

    return sync_detailed(
        client=client,
        multipart_data=multipart_data,
        ttl=ttl,
        image=image,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    multipart_data: UploadFilesMultipartData,
    ttl: Union[Unset, None, int] = 0,
    image: Union[Unset, None, bool] = False,
) -> Response[List[UploadedFile]]:
    """
    Args:
        ttl (Union[Unset, None, int]):
        image (Union[Unset, None, bool]):
        multipart_data (UploadFilesMultipartData):

    Returns:
        Response[List[UploadedFile]]
    """

    kwargs = _get_kwargs(
        client=client,
        multipart_data=multipart_data,
        ttl=ttl,
        image=image,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    multipart_data: UploadFilesMultipartData,
    ttl: Union[Unset, None, int] = 0,
    image: Union[Unset, None, bool] = False,
) -> Optional[List[UploadedFile]]:
    """
    Args:
        ttl (Union[Unset, None, int]):
        image (Union[Unset, None, bool]):
        multipart_data (UploadFilesMultipartData):

    Returns:
        Response[List[UploadedFile]]
    """

    return (
        await asyncio_detailed(
            client=client,
            multipart_data=multipart_data,
            ttl=ttl,
            image=image,
        )
    ).parsed
