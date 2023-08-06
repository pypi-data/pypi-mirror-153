"""
Copyright 2021 Kelvin Inc.

Licensed under the Kelvin Inc. Developer SDK License Agreement (the "License"); you may not use
this file except in compliance with the License.  You may obtain a copy of the
License at

http://www.kelvininc.com/developer-sdk-license

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OF ANY KIND, either express or implied.  See the License for the
specific language governing permissions and limitations under the License.
"""

from typing import Optional

from kelvin.sdk.lib.models.operation import OperationResponse
from kelvin.sdk.server.models.parameter_models import DataTypeCreateRequest, DataTypeUploadRequest
from kelvin.sdk.server.models.router import KelvinSDKServerRouter

router = KelvinSDKServerRouter(
    prefix="/datatypes",
    tags=["Data Types - [kelvin datatype]"],
    responses={404: {"description": "Not found"}},
)


@router.get("")
def datatype_list(query: Optional[str] = None, all_datatypes: bool = False) -> OperationResponse:
    """
    Returns all available of datatypes available on the system.
    """
    if query:
        from kelvin.sdk.interface import datatype_search as _datatype_search

        return _datatype_search(query=query, should_display=False)
    else:
        from kelvin.sdk.interface import datatype_list as _datatype_list

        return _datatype_list(all_datatypes=all_datatypes, query=None, should_display=False)


@router.get("/{datatype_name_with_version}")
def datatype_show(datatype_name_with_version: str) -> OperationResponse:
    """
    Displays the details on a specific datatype.
    """
    from kelvin.sdk.interface import datatype_show as _datatype_show

    return _datatype_show(datatype_name_with_version=datatype_name_with_version, should_display=False)


@router.post("")
def datatype_create(datatype_create_request: DataTypeCreateRequest) -> OperationResponse:
    """
    Creates a datatype from the specified parameters.
    """
    from kelvin.sdk.interface import datatype_create as _datatype_create

    return _datatype_create(
        datatype_name=datatype_create_request.datatype_name, output_dir=datatype_create_request.output_dir
    )


@router.post("/upload")
def datatype_upload(datatype_upload_request: DataTypeUploadRequest) -> OperationResponse:
    """
    Upload all the datatypes in the provided input directory.
    """
    from kelvin.sdk.interface import datatype_upload as _datatype_upload

    return _datatype_upload(input_dir=datatype_upload_request.input_dir, datatypes=datatype_upload_request.datatypes)


@router.get("/download")
def datatype_download(datatype_name_with_version: str, output_dir: str) -> OperationResponse:
    """
    Download the datatype corresponding to the provided datatype id into the provided output dir.
    """
    from kelvin.sdk.interface import datatype_download as _datatype_download

    return _datatype_download(datatype_name_with_version=datatype_name_with_version, output_dir=output_dir)
