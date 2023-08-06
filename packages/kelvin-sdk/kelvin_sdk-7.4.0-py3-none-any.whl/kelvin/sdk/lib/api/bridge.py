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

from typing import List, Optional, cast

from kelvin.sdk.client.error import APIError
from kelvin.sdk.client.model.responses import Bridge
from kelvin.sdk.lib.configs.general_configs import GeneralConfigs
from kelvin.sdk.lib.models.operation import OperationResponse
from kelvin.sdk.lib.session.session_manager import session_manager
from kelvin.sdk.lib.utils.display_utils import DisplayObject, display_data_entries, display_data_object
from kelvin.sdk.lib.utils.exception_utils import retrieve_error_message_from_api_exception
from kelvin.sdk.lib.utils.logger_utils import logger


def bridge_list(query: Optional[str] = None, should_display: bool = False) -> OperationResponse:
    """
    List all available bridges in the platform.

    Parameters
    ----------
    query : str, optional
        The query to search for.
    should_display : bool, Default=False
        Specifies whether or not the display should output data.

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        An OperationResponse object encapsulating the bridges available on the platform.

    """
    try:
        bridge_list_step_1 = "Retrieving bridges.."
        if query:
            bridge_list_step_1 = f'Searching bridges that match "{query}"'

        logger.info(bridge_list_step_1)

        client = session_manager.login_client_on_current_url()

        bridges = cast(List, client.bridge.list_bridge(search=query)) or []

        display_obj = display_data_entries(
            data=bridges,
            header_names=["Name", "Title", "Node name", "Workload name", "Protocol", "Created", "Updated"],
            attributes=["name", "title", "acp_name", "workload_name", "protocol", "created", "updated"],
            table_title=GeneralConfigs.table_title.format(title="Bridges"),
            should_display=should_display,
            no_data_message="No bridges available",
        )

        return OperationResponse(success=True, data=display_obj.parsed_data)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error retrieving bridges: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error retrieving bridges: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def bridge_show(bridge_name: str, should_display: bool = False) -> OperationResponse:
    """
    Show the details of a bridge.

    Parameters
    ----------
    bridge_name : str
        The name of the bridge.
    should_display : bool, Default=False
        Specifies whether or not the display should output data.

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        an OperationResponse object encapsulating the yielded bridge instance and its detailed data.
    """
    try:
        logger.info(f'Retrieving bridge details for "{bridge_name}"')

        client = session_manager.login_client_on_current_url()

        bridge_info: Bridge = client.bridge.get_bridge(bridge_name=bridge_name)
        bridge_info_display: DisplayObject = display_data_object(
            data=bridge_info,
            should_display=should_display,
            object_title=GeneralConfigs.table_title.format(title="Bridge Info"),
        )

        return OperationResponse(success=True, data=bridge_info_display.parsed_data)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error retrieving bridge: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error retrieving bridge: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def bridge_assets(bridge_name: str = None, should_display: bool = False) -> OperationResponse:
    """
    List all assets associated with a specific bridge.

    Parameters
    ----------
    bridge_name : str
        The name of the bridge.
    should_display : bool, Default=False
        Specifies whether or not the display should output data.

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        An OperationResponse object encapsulating assets associated with a specific bridge.

    """
    try:
        logger.info(f'Retrieving bridge assets for "{bridge_name}"..')

        client = session_manager.login_client_on_current_url()

        bridges_assets_data = cast(List, client.bridge.list_bridge_assets(bridge_name=bridge_name)) or []

        display_obj = display_data_entries(
            data=bridges_assets_data,
            header_names=["Asset name", "Title", "Asset Type name", "Created", "Updated"],
            attributes=["name", "title", "asset_type_name", "created", "updated"],
            table_title=GeneralConfigs.table_title.format(title="Bridge Assets"),
            should_display=should_display,
            no_data_message="No bridge assets available",
        )

        return OperationResponse(success=True, data=display_obj.parsed_data)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error retrieving bridge assets: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error retrieving bridge assets: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def bridge_streams(bridge_name: str = None, should_display: bool = False) -> OperationResponse:
    """
    List all data streams associated with a specific bridge.

    Parameters
    ----------
    bridge_name : str
        The name of the bridge.
    should_display : bool, Default=False
        Specifies whether or not the display should output data.

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        An OperationResponse object encapsulating data streams associated with a specific bridge.

    """
    try:
        logger.info(f'Retrieving bridge data streams for "{bridge_name}"..')

        client = session_manager.login_client_on_current_url()

        bridge_streams_data = cast(List, client.bridge.list_bridge_data_streams(bridge_name=bridge_name)) or []

        display_obj = display_data_entries(
            data=bridge_streams_data,
            header_names=["Metric name", "Asset name", "Payload"],
            attributes=["metric_name", "asset_name", "payload"],
            table_title=GeneralConfigs.table_title.format(title="Bridge Data Streams"),
            should_display=should_display,
            no_data_message="No bridge data streams available",
        )

        return OperationResponse(success=True, data=display_obj.parsed_data)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error retrieving bridge data streams: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error retrieving bridge data streams: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def bridge_metrics(bridge_name: str = None, should_display: bool = False) -> OperationResponse:
    """
    List all metrics associated with a specific bridge.

    Parameters
    ----------
    bridge_name : str
        The name of the bridge.
    should_display : bool, Default=False
        Specifies whether or not the display should output data.

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        An OperationResponse object encapsulating metrics associated with a specific bridge.

    """
    try:
        logger.info(f'Retrieving bridge metrics for "{bridge_name}"..')

        client = session_manager.login_client_on_current_url()

        bridges_metrics_data = cast(List, client.bridge.list_bridge_metrics(bridge_name=bridge_name)) or []

        display_obj = display_data_entries(
            data=bridges_metrics_data,
            header_names=[
                "Metric Name",
                "Title",
                "Display unit",
                "Data type",
                "Data type version",
                "Created",
                "Updated",
            ],
            attributes=["name", "title", "display_unit", "data_type_name", "data_type_version", "created", "updated"],
            table_title=GeneralConfigs.table_title.format(title="Bridge Metrics"),
            should_display=should_display,
            no_data_message="No bridge metrics available",
        )

        return OperationResponse(success=True, data=display_obj.parsed_data)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error retrieving bridge metrics: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error retrieving bridge metrics: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)
