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

from typing import List, Optional

from typeguard import typechecked

from kelvin.sdk.lib.models.operation import OperationResponse


@typechecked
def datatype_list(
    query: Optional[str] = None, all_datatypes: bool = False, should_display: bool = False
) -> OperationResponse:
    """
    Returns all available of data types available on the system.

    Parameters
    ----------
    query: Optional[str]
        the query to search for.
    all_datatypes: bool
        Indicates whether the list operation should yield all data types and its respective versions.
    should_display: bool
        specifies whether or not the display should output data.

    Returns
    ----------
    kelvin.sdk.lib.models.operation.OperationResponse
        an OperationResponse object encapsulating the data types available on the platform.

    """
    from kelvin.sdk.lib.api.datatype import datatype_list as _datatype_list

    return _datatype_list(all_datatypes=all_datatypes, query=query, should_display=should_display)


@typechecked
def datatype_search(query: Optional[str] = None, should_display: bool = False) -> OperationResponse:
    """
    Search for data types on the platform that match the provided query.

    Parameters
    ----------
    query: Optional[str]
        the query to search for.
    should_display: bool
        specifies whether or not the display should output data.

    Returns
    ----------
    kelvin.sdk.lib.models.operation.OperationResponse
        an OperationResponse object encapsulating the matching data types available on the platform.

    """
    from kelvin.sdk.lib.api.datatype import datatype_list as _datatype_list

    return _datatype_list(all_datatypes=True, query=query, should_display=should_display)


@typechecked
def datatype_show(datatype_name_with_version: str, should_display: bool = True) -> OperationResponse:
    """
    Displays the details on a specific datatype.

    Parameters
    ----------
    datatype_name_with_version: str
        the name with version of the datatype to show.
    should_display: bool
        specifies whether or not the display should output data.

    Returns
    ----------
    kelvin.sdk.lib.models.operation.OperationResponse
        an OperationResponse object encapsulating the yielded data type and its data.

    """
    from kelvin.sdk.lib.api.datatype import datatype_show as _datatype_show

    return _datatype_show(datatype_name_with_version=datatype_name_with_version, should_display=should_display)


@typechecked
def datatype_create(datatype_name: str, output_dir: Optional[str] = None) -> OperationResponse:
    """
    Creates a data type from the specified parameters.

    Parameters
    ----------
    datatype_name: str
        the name of the datatype to create.
    output_dir: Optional[str]
        the output directory where the data type will be created.

    Returns
    ----------
    kelvin.sdk.lib.models.operation.OperationResponse
        an OperationResponse object encapsulating the result of the data type creation operation.

    """
    from kelvin.sdk.lib.datatypes.datatypes_manager import create_datatype as _create_datatype

    return _create_datatype(datatype_name=datatype_name, output_dir=output_dir)


@typechecked
def datatype_upload(input_dir: Optional[str] = None, datatypes: Optional[List[str]] = None) -> OperationResponse:
    """
    Upload all the data types in the provided input directory.

    Parameters
    ----------
    input_dir: Optional[str]
        the directory to read the data types from.
    datatypes: Optional[List[str]]
        the names of the data types to upload.

    Returns
    ----------
    kelvin.sdk.lib.models.operation.OperationResponse
        an OperationResponse object encapsulating the result of the data type upload operation.

    """
    from kelvin.sdk.lib.datatypes.datatypes_manager import upload_datatypes as _upload_datatypes

    return _upload_datatypes(input_dir=input_dir, datatypes=datatypes)


@typechecked
def datatype_download(datatype_name_with_version: str, output_dir: Optional[str] = None) -> OperationResponse:
    """
    Download the datatype corresponding to the provided data type id into the provided output dir.

    Parameters
    ----------
    datatype_name_with_version: str
        the name with version of the data type to download.
    output_dir: Optional[str]
        the path into which the data types should be downloaded.

    Returns
    ----------
    kelvin.sdk.lib.models.operation.OperationResponse
        an OperationResponse object encapsulating the result of the data type download operation.

    """
    from kelvin.sdk.lib.datatypes.datatypes_manager import download_datatype as _download_datatype

    return _download_datatype(datatype_name_with_version=datatype_name_with_version, output_dir=output_dir)
