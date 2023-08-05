from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.launch_document_import_multipart_data import LaunchDocumentImportMultipartData
from ...models.launch_document_import_segmentation_policy import LaunchDocumentImportSegmentationPolicy
from ...models.sherpa_job_bean import SherpaJobBean
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
    multipart_data: LaunchDocumentImportMultipartData,
    ignore_labelling: Union[Unset, None, bool] = False,
    segmentation_policy: Union[
        Unset, None, LaunchDocumentImportSegmentationPolicy
    ] = LaunchDocumentImportSegmentationPolicy.COMPUTE_IF_MISSING,
    split_corpus: Union[Unset, None, bool] = False,
    clean_text: Union[Unset, None, bool] = True,
    generate_categories_from_source_folder: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/documents".format(client.base_url, projectName=project_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["ignoreLabelling"] = ignore_labelling

    json_segmentation_policy: Union[Unset, None, str] = UNSET
    if not isinstance(segmentation_policy, Unset):
        json_segmentation_policy = segmentation_policy.value if segmentation_policy else None

    params["segmentationPolicy"] = json_segmentation_policy

    params["splitCorpus"] = split_corpus

    params["cleanText"] = clean_text

    params["generateCategoriesFromSourceFolder"] = generate_categories_from_source_folder

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


def _parse_response(*, response: httpx.Response) -> Optional[SherpaJobBean]:
    if response.status_code == 200:
        response_200 = SherpaJobBean.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[SherpaJobBean]:
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
    multipart_data: LaunchDocumentImportMultipartData,
    ignore_labelling: Union[Unset, None, bool] = False,
    segmentation_policy: Union[
        Unset, None, LaunchDocumentImportSegmentationPolicy
    ] = LaunchDocumentImportSegmentationPolicy.COMPUTE_IF_MISSING,
    split_corpus: Union[Unset, None, bool] = False,
    clean_text: Union[Unset, None, bool] = True,
    generate_categories_from_source_folder: Union[Unset, None, bool] = False,
) -> Response[SherpaJobBean]:
    """upload documents and launch a job to add them into the project

    Args:
        project_name (str):
        ignore_labelling (Union[Unset, None, bool]):
        segmentation_policy (Union[Unset, None, LaunchDocumentImportSegmentationPolicy]):
            Default: LaunchDocumentImportSegmentationPolicy.COMPUTE_IF_MISSING.
        split_corpus (Union[Unset, None, bool]):
        clean_text (Union[Unset, None, bool]):  Default: True.
        generate_categories_from_source_folder (Union[Unset, None, bool]):
        multipart_data (LaunchDocumentImportMultipartData):

    Returns:
        Response[SherpaJobBean]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        multipart_data=multipart_data,
        ignore_labelling=ignore_labelling,
        segmentation_policy=segmentation_policy,
        split_corpus=split_corpus,
        clean_text=clean_text,
        generate_categories_from_source_folder=generate_categories_from_source_folder,
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
    multipart_data: LaunchDocumentImportMultipartData,
    ignore_labelling: Union[Unset, None, bool] = False,
    segmentation_policy: Union[
        Unset, None, LaunchDocumentImportSegmentationPolicy
    ] = LaunchDocumentImportSegmentationPolicy.COMPUTE_IF_MISSING,
    split_corpus: Union[Unset, None, bool] = False,
    clean_text: Union[Unset, None, bool] = True,
    generate_categories_from_source_folder: Union[Unset, None, bool] = False,
) -> Optional[SherpaJobBean]:
    """upload documents and launch a job to add them into the project

    Args:
        project_name (str):
        ignore_labelling (Union[Unset, None, bool]):
        segmentation_policy (Union[Unset, None, LaunchDocumentImportSegmentationPolicy]):
            Default: LaunchDocumentImportSegmentationPolicy.COMPUTE_IF_MISSING.
        split_corpus (Union[Unset, None, bool]):
        clean_text (Union[Unset, None, bool]):  Default: True.
        generate_categories_from_source_folder (Union[Unset, None, bool]):
        multipart_data (LaunchDocumentImportMultipartData):

    Returns:
        Response[SherpaJobBean]
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        multipart_data=multipart_data,
        ignore_labelling=ignore_labelling,
        segmentation_policy=segmentation_policy,
        split_corpus=split_corpus,
        clean_text=clean_text,
        generate_categories_from_source_folder=generate_categories_from_source_folder,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Client,
    multipart_data: LaunchDocumentImportMultipartData,
    ignore_labelling: Union[Unset, None, bool] = False,
    segmentation_policy: Union[
        Unset, None, LaunchDocumentImportSegmentationPolicy
    ] = LaunchDocumentImportSegmentationPolicy.COMPUTE_IF_MISSING,
    split_corpus: Union[Unset, None, bool] = False,
    clean_text: Union[Unset, None, bool] = True,
    generate_categories_from_source_folder: Union[Unset, None, bool] = False,
) -> Response[SherpaJobBean]:
    """upload documents and launch a job to add them into the project

    Args:
        project_name (str):
        ignore_labelling (Union[Unset, None, bool]):
        segmentation_policy (Union[Unset, None, LaunchDocumentImportSegmentationPolicy]):
            Default: LaunchDocumentImportSegmentationPolicy.COMPUTE_IF_MISSING.
        split_corpus (Union[Unset, None, bool]):
        clean_text (Union[Unset, None, bool]):  Default: True.
        generate_categories_from_source_folder (Union[Unset, None, bool]):
        multipart_data (LaunchDocumentImportMultipartData):

    Returns:
        Response[SherpaJobBean]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        multipart_data=multipart_data,
        ignore_labelling=ignore_labelling,
        segmentation_policy=segmentation_policy,
        split_corpus=split_corpus,
        clean_text=clean_text,
        generate_categories_from_source_folder=generate_categories_from_source_folder,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    project_name: str,
    *,
    client: Client,
    multipart_data: LaunchDocumentImportMultipartData,
    ignore_labelling: Union[Unset, None, bool] = False,
    segmentation_policy: Union[
        Unset, None, LaunchDocumentImportSegmentationPolicy
    ] = LaunchDocumentImportSegmentationPolicy.COMPUTE_IF_MISSING,
    split_corpus: Union[Unset, None, bool] = False,
    clean_text: Union[Unset, None, bool] = True,
    generate_categories_from_source_folder: Union[Unset, None, bool] = False,
) -> Optional[SherpaJobBean]:
    """upload documents and launch a job to add them into the project

    Args:
        project_name (str):
        ignore_labelling (Union[Unset, None, bool]):
        segmentation_policy (Union[Unset, None, LaunchDocumentImportSegmentationPolicy]):
            Default: LaunchDocumentImportSegmentationPolicy.COMPUTE_IF_MISSING.
        split_corpus (Union[Unset, None, bool]):
        clean_text (Union[Unset, None, bool]):  Default: True.
        generate_categories_from_source_folder (Union[Unset, None, bool]):
        multipart_data (LaunchDocumentImportMultipartData):

    Returns:
        Response[SherpaJobBean]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            multipart_data=multipart_data,
            ignore_labelling=ignore_labelling,
            segmentation_policy=segmentation_policy,
            split_corpus=split_corpus,
            clean_text=clean_text,
            generate_categories_from_source_folder=generate_categories_from_source_folder,
        )
    ).parsed
