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

from typing import List, Optional, Sequence, cast

from kelvin.sdk.client.error import APIError
from kelvin.sdk.client.model.requests import AssetCreateWithParent, AssetTypeCreate
from kelvin.sdk.client.model.responses import Asset, AssetType
from kelvin.sdk.lib.configs.general_configs import GeneralConfigs
from kelvin.sdk.lib.models.apps.kelvin_app import DeviceTypeName
from kelvin.sdk.lib.models.operation import OperationResponse
from kelvin.sdk.lib.session.session_manager import session_manager
from kelvin.sdk.lib.utils.display_utils import (
    DisplayObject,
    display_data_entries,
    display_data_object,
    display_yes_or_no_question,
)
from kelvin.sdk.lib.utils.exception_utils import retrieve_error_message_from_api_exception
from kelvin.sdk.lib.utils.logger_utils import logger


def asset_list(query: Optional[str] = None, should_display: bool = False) -> OperationResponse:
    """
    List all the available assets in the platform.

    Parameters
    ----------
    query : str, optional
        The query to search for.
    should_display : bool, Default=False
        Specifies whether or not the display should output data.

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        An OperationResponse object encapsulating the Assets available on the platform.

    """
    try:
        asset_list_step_1 = "Retrieving assets.."
        if query:
            asset_list_step_1 = f'Searching assets that match "{query}"'

        logger.info(asset_list_step_1)

        client = session_manager.login_client_on_current_url()

        assets = cast(List, client.asset.list_asset(search=query)) or []

        display_obj = display_data_entries(
            data=assets,
            header_names=["Name", "Title", "Asset Type", "Created", "Updated"],
            attributes=["name", "title", "asset_type_name", "created", "updated"],
            table_title=GeneralConfigs.table_title.format(title="Assets"),
            should_display=should_display,
            no_data_message="No assets available",
        )

        return OperationResponse(success=True, data=display_obj.parsed_data)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error retrieving assets: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error retrieving assets: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def asset_show(asset_name: str, should_display: bool = False) -> OperationResponse:
    """
    Show the details of an Asset.

    Parameters
    ----------
    asset_name : str
        The name of the asset.
    should_display : bool, Default=False
        Specifies whether or not the display should output data.

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        an OperationResponse object encapsulating the yielded Asset instance and its detailed data.
    """
    try:
        logger.info(f'Retrieving asset details for "{asset_name}"')

        client = session_manager.login_client_on_current_url()

        asset_info: Asset = client.asset.get_asset(asset_name=asset_name)
        asset_info_display: DisplayObject = display_data_object(
            data=asset_info,
            should_display=should_display,
            object_title=GeneralConfigs.table_title.format(title="Asset Info"),
        )

        return OperationResponse(success=True, data=asset_info_display.parsed_data)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error retrieving asset: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error retrieving asset: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def asset_create(
    asset_name: str,
    asset_type_name: str,
    asset_title: str,
    entity_type_name: DeviceTypeName,
    parent_name: Optional[str] = None,
) -> OperationResponse:
    """
    Create an Asset on the platform.

    Parameters
    ----------
    asset_name : str
        The name of the asset.
    asset_type_name : str
        The asset type name of the asset.
    asset_title : str
        The title of the asset.
    entity_type_name : DeviceTypeName
        The device type of the asset.
    parent_name : Optional[str]
        Optional parent name of the created asset

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        An OperationResponse object encapsulating the result of an Asset creation operation.

    """
    try:
        logger.info(f'Create new Asset "{asset_name}"')

        client = session_manager.login_client_on_current_url()

        asset_create_request = AssetCreateWithParent(
            name=asset_name,
            title=asset_title,
            asset_type_name=asset_type_name,
            entity_type_name=entity_type_name.value,
            parent_name=parent_name,
        )
        asset_info: Asset = client.asset.create_asset(data=asset_create_request)

        success_message = f'Asset "{asset_info.name}" successfully created'
        logger.relevant(success_message)

        return OperationResponse(success=True, log=success_message)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error creating asset: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error creating asset: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def asset_delete(asset_names: Sequence[str], ignore_destructive_warning: bool = False) -> OperationResponse:
    """
    Delete Assets from the platform.

    Parameters
    ----------
    asset_names : Sequence[str]
        The name of the asset.
    ignore_destructive_warning : bool, Default=False
        Indicates whether it should ignore the destructive warning.

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        An OperationResponse object encapsulating the result of the Asset deletion operation.

    """
    assets_description = ", ".join(asset_names)
    logger.info(f'Deleting Asset(s) "{assets_description}" from the platform')

    prompt_question = f'This operation will delete the assets(s) "{assets_description}" from the platform'
    if not ignore_destructive_warning:
        ignore_destructive_warning = display_yes_or_no_question(question=prompt_question)

    if ignore_destructive_warning:
        client = session_manager.login_client_on_current_url()
        for asset in asset_names:
            try:
                client.asset.delete_asset(asset_name=asset)
                logger.relevant(f'Asset "{asset}" successfully deleted from the platform')

            except APIError as exc:
                api_error = retrieve_error_message_from_api_exception(api_error=exc)
                api_error_message = f"Error deleting asset: {api_error}"
                logger.error(api_error_message)
                return OperationResponse(success=False, log=api_error_message)

            except Exception as exc:
                error_message = f"Error deleting asset: {str(exc)}"
                logger.exception(error_message)
                return OperationResponse(success=False, log=error_message)

    return OperationResponse(success=True, log="Successfully deleted assets")


def asset_type_list(query: Optional[str] = None, should_display: bool = False) -> OperationResponse:
    """
    List all the available Asset Types in the platform.

    Parameters
    ----------
    query : str, optional
        The query to search for.
    should_display : bool, Default=False
        Specifies whether or not the display should output data.

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        An OperationResponse object encapsulating the Asset types available on the platform.

    """
    try:
        asset_list_step_1 = "Retrieving asset types.."
        if query:
            asset_list_step_1 = f'Searching asset types that match "{query}"'

        logger.info(asset_list_step_1)

        client = session_manager.login_client_on_current_url()

        assets = cast(List, client.asset_type.list_asset_type(search=query)) or []

        display_obj = display_data_entries(
            data=assets,
            header_names=["Asset Type Name", "Title", "Metadata", "Created", "Updated"],
            attributes=["name", "title", "metadata", "created", "updated"],
            table_title=GeneralConfigs.table_title.format(title="Asset types"),
            should_display=should_display,
            no_data_message="No asset types available",
        )

        return OperationResponse(success=True, data=display_obj.parsed_data)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error retrieving asset types: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error retrieving asset types: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def asset_type_create(asset_type_name: str, asset_type_title: str, asset_class_name: str) -> OperationResponse:
    """
    Create an Asset Type on the platform.

    Parameters
    ----------
    asset_type_name : str
        The name of the asset type.
    asset_type_title : str
        The title to be associated to the asset type.
    asset_class_name : str
        The asset class name associated to the new asset type.

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        An OperationResponse object encapsulating the result of the Asset type creation operation.

    """
    try:
        logger.info(f'Create new asset type "{asset_type_name}"')

        client = session_manager.login_client_on_current_url()

        asset_type_create_request = AssetTypeCreate(
            name=asset_type_name, title=asset_type_title, asset_class_name=asset_class_name
        )
        asset_type_info: AssetType = client.asset_type.create_asset_type(data=asset_type_create_request)

        success_message = f'Asset type "{asset_type_info.name}" successfully created'
        logger.relevant(success_message)

        return OperationResponse(success=True, log=success_message)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error creating asset type: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error creating asset type: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def asset_type_delete(asset_type_names: Sequence[str], ignore_destructive_warning: bool = False) -> OperationResponse:
    """
    Delete Asset types from the platform.

    Parameters
    ----------
    asset_type_names : Sequence[str]
        The name of the asset types.
    ignore_destructive_warning : bool, Default=False
        Indicates whether it should ignore the destructive warning.

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        An OperationResponse object encapsulating the result of the Asset type deletion operation.

    """
    assets_types_description = ", ".join(asset_type_names)
    logger.info(f'Deleting asset type(s) "{assets_types_description}" from the platform')

    prompt_question = f'This operation will delete the assets type(s) "{assets_types_description}" from the platform'
    if not ignore_destructive_warning:
        ignore_destructive_warning = display_yes_or_no_question(question=prompt_question)

    if ignore_destructive_warning:
        client = session_manager.login_client_on_current_url()
        for asset_type_name in asset_type_names:
            try:
                client.asset_type.delete_asset_type(asset_type_name=asset_type_name)
                logger.relevant(f'Asset type "{asset_type_name}" successfully deleted from the platform')

            except APIError as exc:
                api_error = retrieve_error_message_from_api_exception(api_error=exc)
                api_error_message = f"Error deleting asset type: {api_error}"
                logger.error(api_error_message)
                return OperationResponse(success=False, log=api_error_message)

            except Exception as exc:
                error_message = f"Error deleting asset type: {str(exc)}"
                logger.exception(error_message)
                return OperationResponse(success=False, log=error_message)

    return OperationResponse(success=True, log="Successfully deleted asset types")
