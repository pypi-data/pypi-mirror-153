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

from typing import Dict, List, Optional, cast

from kelvin.sdk.client.error import APIError
from kelvin.sdk.client.model.requests import DataTypeCreate, ICDPayload
from kelvin.sdk.client.model.responses import DataType
from kelvin.sdk.lib.configs.general_configs import GeneralConfigs
from kelvin.sdk.lib.models.datatypes import ICDPayloadHelper
from kelvin.sdk.lib.models.generic import KPath
from kelvin.sdk.lib.models.ksdk_docker import DockerImageName
from kelvin.sdk.lib.models.operation import OperationResponse
from kelvin.sdk.lib.session.session_manager import session_manager
from kelvin.sdk.lib.utils.datatype_utils import check_if_datatype_name_with_version_is_valid
from kelvin.sdk.lib.utils.display_utils import display_data_entries, display_data_object
from kelvin.sdk.lib.utils.exception_utils import retrieve_error_message_from_api_exception
from kelvin.sdk.lib.utils.logger_utils import logger


def datatype_list(
    query: Optional[str] = None, all_datatypes: bool = False, should_display: bool = False
) -> OperationResponse:
    """
    Returns all available of data types available on the system.

    Parameters
    ----------
    query: str, optional
        The query to search for.
    all_datatypes: bool, default=False
        Indicates whether the list operation should yield all data types and its respective versions.
    should_display: bool, default=False
        Specifies whether or not the display should output data.

    Returns
    -------
    kelvin.sdk.lib.common.models.operation.OperationResponse
        An OperationResponse object encapsulating the data types available on the platform.

    """
    try:
        datatype_list_step_1 = "Retrieving data types.."
        if query:
            datatype_list_step_1 = f'Searching datatypes that match "{query}"'

        logger.info(datatype_list_step_1)

        client = session_manager.login_client_on_current_url()

        datatypes = cast(List, client.data_type.list_data_type(search=query, all=all_datatypes)) or []

        display_obj = display_data_entries(
            data=datatypes,
            header_names=["Model", "Type", "Version", "Created", "Updated"],
            attributes=["name", "type", "version", "updated", "created"],
            table_title=GeneralConfigs.table_title.format(title="Data types"),
            should_display=should_display,
            no_data_message="No data types available",
        )

        return OperationResponse(success=True, data=display_obj.parsed_data)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error retrieving data types: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error listing data types: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def datatype_show(datatype_name_with_version: str, should_display: bool = False) -> OperationResponse:
    """
    Displays the details on a specific datatype.

    Parameters
    ----------
    datatype_name_with_version : str
        The name with version of the datatype to show.
    should_display : bool, Default=False
        Specifies whether or not the display should output data.

    Returns
    ----------
    kelvin.sdk.lib.common.models.operation.OperationResponse
        An OperationResponse object encapsulating the yielded data type and its data.

    """
    try:
        check_if_datatype_name_with_version_is_valid(app_name_with_version=datatype_name_with_version)

        client = session_manager.login_client_on_current_url()
        name_with_version = DockerImageName.parse(name=datatype_name_with_version)

        if not name_with_version.version:
            datatype = client.data_type.get_data_type_latest_version(data_type_name=datatype_name_with_version)
        else:
            datatype = client.data_type.get_data_type(
                data_type_name=name_with_version.name, data_type_version=name_with_version.version
            )
        logger.info(f'Retrieving data type "{name_with_version.repository_image_name}"')

        title = GeneralConfigs.table_title.format(title="Data type Info")
        datatype_data_display_object = display_data_object(
            data=datatype, should_display=should_display, object_title=title
        )

        return OperationResponse(success=True, data=datatype_data_display_object.parsed_data)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error showing data type: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error showing data type: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def datatype_upload(datatype_content: Dict, source: str) -> OperationResponse:
    """
    Upload a single data type to the platform, along with its corresponding source.

    Parameters
    ----------
    datatype_content: Dict
        The data type to upload to the platform.
    source: str
        The source corresponding to the data type.

    Returns
    -------
    kelvin.sdk.lib.common.models.operation.OperationResponse
        An OperationResponse object encapsulating the result of the data types upload operation.

    """
    try:
        client = session_manager.login_client_on_current_url()

        icd_payload_helper = ICDPayloadHelper(**datatype_content)

        datatype_name_with_version = f"{icd_payload_helper.name}:{icd_payload_helper.version}"
        logger.info(f'Uploading data type "{datatype_name_with_version}"')

        icd_payload = ICDPayload(**icd_payload_helper.dict())
        datatype_create_payload = DataTypeCreate(icd=icd_payload, source=source)
        client.data_type.create_data_type(data=datatype_create_payload)

        success_message = f'Data type "{icd_payload.name}" successfully uploaded'
        logger.relevant(success_message)

        return OperationResponse(success=True, log=success_message)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error uploading data type: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error uploading data type: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def datatype_download(datatype_name: str, datatype_version: str, output_dir: str) -> Optional[ICDPayloadHelper]:
    """
    Download the data type corresponding to the provided data type id into the provided output directory.

    Parameters
    ----------
    datatype_name: str
        The name of the data type to download.
    datatype_version: str
        The version of the data type to download.
    output_dir: str
        The path into which the data type should be downloaded.

    Returns
    -------
    kelvin.sdk.lib.common.models.datatypes.ICDPayloadHelper, optional
        An ICDPayloadHelper object.

    """
    try:
        _client = session_manager.login_client_on_current_url()

        full_datatype_name = f"{datatype_name.strip()}:{datatype_version.strip()}".strip()

        logger.info(f'Downloading data type "{full_datatype_name}"')

        # 1 - retrieve the data type and write it
        datatype: DataType = _client.data_type.get_data_type(
            data_type_name=datatype_name, data_type_version=datatype_version
        )
        # 2 - Despite the ICD definition being mandatory, its model states it is
        if datatype.icd:
            # 3 - data type path and structure
            icd_payload_helper = ICDPayloadHelper(**datatype.icd)
            output_path = KPath(output_dir) if output_dir else KPath("")
            output_path.create_dir()
            datatype_path: KPath = output_path / icd_payload_helper.datatype_file_name

            datatype_path.write_yaml(yaml_data=icd_payload_helper.dict(exclude_none=True))
            message = f'Data type "{full_datatype_name}" successfully downloaded to "{datatype_path}"'
            logger.relevant(message)
            return icd_payload_helper

    except APIError as exc:
        error_message = retrieve_error_message_from_api_exception(api_error=exc)
        logger.error(f'Error downloading data type "{datatype_name}:{datatype_version}": {error_message}')

    except Exception as exc:
        logger.exception(f"Error downloading data type: {str(exc)}")

    return None
