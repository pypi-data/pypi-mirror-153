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
from kelvin.sdk.client.model.responses import ACP as Node  # noqa: N811
from kelvin.sdk.client.model.responses import ACPStatus as NodeStatus
from kelvin.sdk.client.model.responses import ACPTelemetry as NodeTelemetry
from kelvin.sdk.lib.api.workload import retrieve_workload_and_workload_status_data
from kelvin.sdk.lib.configs.general_configs import GeneralConfigs, GeneralMessages
from kelvin.sdk.lib.models.generic import GenericObject
from kelvin.sdk.lib.models.operation import OperationResponse
from kelvin.sdk.lib.models.types import StatusDataSource
from kelvin.sdk.lib.session.session_manager import session_manager
from kelvin.sdk.lib.utils.display_utils import (
    DisplayObject,
    display_data_entries,
    display_data_object,
    display_yes_or_no_question,
    error_colored_message,
    success_colored_message,
    warning_colored_message,
)
from kelvin.sdk.lib.utils.exception_utils import retrieve_error_message_from_api_exception
from kelvin.sdk.lib.utils.general_utils import get_bytes_as_human_readable, get_datetime_as_human_readable
from kelvin.sdk.lib.utils.logger_utils import logger


def node_list(query: Optional[str] = None, should_display: bool = False) -> OperationResponse:
    """
    Search for nodes on the platform that match the provided query.

    Parameters
    ----------
    query: Optional[str]
        the query to search for.
    should_display: bool
        specifies whether or not the display should output data.

    Returns
    ----------
    OperationResponse
        an OperationResponse object encapsulating the matching nodes available on the platform.

    """
    try:
        node_list_step_1 = "Retrieving nodes.."
        if query:
            node_list_step_1 = f'Searching nodes that match "{query}"'

        logger.info(node_list_step_1)

        display_obj: DisplayObject = retrieve_node_and_node_status_data(
            query=query, should_display=should_display, should_colorize=should_display
        )

        return OperationResponse(success=True, data=display_obj.parsed_data)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error retrieving nodes: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error retrieving nodes: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def node_show(
    node_name: str, source: StatusDataSource = StatusDataSource.CACHE, should_display: bool = False
) -> OperationResponse:
    """
    Displays all the details of the specified node from the platform.

    Parameters
    ----------
    node_name: str
        the name of the node.
    source: StatusDataSource
        the status data source from where to obtain data.
    should_display: bool
        specifies whether or not the display should output data.

    Returns
    ----------
    OperationResponse
        an OperationResponse object encapsulating the yielded node instance and its detailed data.

    """
    try:
        logger.info(f'Retrieving node details for "{node_name}"')

        client = session_manager.login_client_on_current_url()

        # 1 - Retrieve the node data
        node_info: Node = client.acp.get_acp(acp_name=node_name)  # camouflaged
        node_info_display: DisplayObject = display_data_object(
            data=node_info, object_title=GeneralConfigs.table_title.format(title="Node Info"), should_display=False
        )

        # 2 - If enabled, retrieve the node metrics
        node_metrics_display_output: str = ""
        node_telemetry_data_display: Optional[DisplayObject] = None

        logger.info(f'Node metrics available. Retrieving metrics for "{node_name}"')
        node_telemetry_data = client.acp_telemetry.get_acp_telemetry(acp_name=node_name)  # camouflaged
        node_telemetry_data_display = retrieve_node_telemetry_data(
            node_telemetry_data=node_telemetry_data, title="Node Telemetry"
        )
        node_metrics_display_output = node_telemetry_data_display.tabulated_data

        # 3 - Retrieve the workload data corresponding to the node
        workloads_display = retrieve_workload_and_workload_status_data(
            node_name=node_name, source=source, should_display=False
        )
        node_info_display_output = node_info_display.tabulated_data

        workloads_display_output = workloads_display.tabulated_data

        if should_display:
            logger.info(f"{node_info_display_output}\n{node_metrics_display_output}\n{workloads_display_output}")

        complete_node_info = {}
        if node_info_display:
            complete_node_info["node"] = node_info_display.parsed_data
        if node_telemetry_data_display:
            complete_node_info["node_telemetry"] = node_telemetry_data_display.parsed_data
        if workloads_display:
            complete_node_info["node_workloads"] = workloads_display.parsed_data

        return OperationResponse(success=True, data=complete_node_info)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error retrieving node: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error retrieving node: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def node_delete(node_name: str, ignore_destructive_warning: bool = False) -> OperationResponse:
    """
    Delete a node from the platform.

    Parameters
    ----------
    node_name: str
        the name of the node to delete.
    ignore_destructive_warning: bool
        indicates whether it should ignore the destructive warning.

    Returns
    ----------
    OperationResponse
        an OperationResponse object encapsulating the result of the node deletion operation.

    """
    try:
        if not ignore_destructive_warning:
            node_delete_confirmation: str = """
                This operation will remove the node from the platform.
                The node's local data will be lost.
            """
            ignore_destructive_warning = display_yes_or_no_question(node_delete_confirmation)

        success_message = ""
        if ignore_destructive_warning:
            logger.info(f'Deleting node "{node_name}"')

            client = session_manager.login_client_on_current_url()

            client.acp.delete_acp(acp_name=node_name)  # camouflaged

            success_message = f'Node "{node_name}" successfully deleted'
            logger.relevant(success_message)

        return OperationResponse(success=True, log=success_message)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error deleting node: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error deleting node: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def retrieve_node_telemetry_data(node_telemetry_data: NodeTelemetry, title: str = "") -> DisplayObject:
    """
    Unpack the data provided by the NodeMetrics object.

    Parameters
    ----------
    node_telemetry_data : NodeTelemetry
        the NodeTelemetry object.
    title : str
        the title to associate to the the node metrics detail info.

    Returns
    -------
    DisplayObject
        a DisplayObject containing a simplified, pretty metrics object.

    """
    final_object: dict = {}

    allocation_data = node_telemetry_data.allocation
    cpu_utilization_data = node_telemetry_data.cpu_utilization
    disk_data = node_telemetry_data.disk
    memory_usage_data = node_telemetry_data.memory_usage
    network_data = node_telemetry_data.network

    if allocation_data:
        final_object["Allocation"] = {
            "CPU capacity": allocation_data.cpu_capacity,
            "CPU usage": allocation_data.cpu_requests,
            "Memory capacity": get_bytes_as_human_readable(input_bytes_data=allocation_data.memory_capacity),
            "Memory usage": get_bytes_as_human_readable(input_bytes_data=allocation_data.memory_requests),
        }

    if cpu_utilization_data:
        last_cpu_utilization_entry = cpu_utilization_data[-1] if cpu_utilization_data else None
        if last_cpu_utilization_entry:
            final_object["CPU utilization"] = {
                "Timestamp (date)": get_datetime_as_human_readable(input_date=last_cpu_utilization_entry.timestamp),
                "Value": last_cpu_utilization_entry.value,
            }

    if disk_data:
        final_object["Disk data"] = {
            "Total capacity": get_bytes_as_human_readable(input_bytes_data=disk_data.total_bytes),
            "Used capacity": get_bytes_as_human_readable(input_bytes_data=disk_data.used_bytes),
        }

    if memory_usage_data:
        last_memory_usage_entry = memory_usage_data[-1] if memory_usage_data else None
        if last_memory_usage_entry:
            final_object["Memory usage"] = {
                "Timestamp (date)": get_datetime_as_human_readable(input_date=last_memory_usage_entry.timestamp),
                "Value": get_bytes_as_human_readable(input_bytes_data=last_memory_usage_entry.value),
            }

    if network_data:
        final_object["Network data"] = {
            "Transmitted (Tx)": get_bytes_as_human_readable(input_bytes_data=network_data.total_tx),
            "Received (Rx)": get_bytes_as_human_readable(input_bytes_data=network_data.total_rx),
        }

    return display_data_object(data=final_object, object_title=title, should_display=False)


def retrieve_node_and_node_status_data(
    query: Optional[str] = None,
    should_display: bool = True,
    should_colorize: bool = True,
) -> DisplayObject:
    """
    Centralize all calls to nodes.
    Retrieve all nodes that match the provided criteria.

    Parameters
    ----------
    query: Optional[str]
        the query to search specific nodes.
    should_display: bool
        if specified, will display the results of this retrieve operation.
    should_colorize: bool
        if set to False, will return the contents in its raw format.

    Returns
    -------
    DisplayObject
        a DisplayObject containing the nodes and respective status data.

    """
    client = session_manager.login_client_on_current_url()

    nodes = cast(List, client.acp_item.list_acp(search=query))  # camouflaged
    data_to_display = [
        {
            "name": node.name,
            "title": node.title,
            "status": _get_parsed_node_status(node.status, should_colorize=should_colorize),
            "last_seen": get_datetime_as_human_readable(input_date=node.status.last_seen),
        }
        for node in nodes
    ]

    return display_data_entries(
        data=data_to_display,
        header_names=["Name", "Title", "Node Status", "Last seen"],
        attributes=["name", "title", "status", "last_seen"],
        table_title=GeneralConfigs.table_title.format(title="Nodes"),
        should_display=should_display,
        no_data_message="No nodes available",
    )


def _get_parsed_node_status(node_status_item: Optional[NodeStatus] = None, should_colorize: bool = True) -> str:
    """
    When provided with an NodeStatus, yield the message the message with the provided color schema and format.

    Parameters
    ----------
    node_status_item: Optional[NodeStatus]
        the Nodes status item containing all necessary information.
    should_colorize: bool
        if set to False, will return the contents in its raw format.

    Returns
    -------
    str
        a formatted string with the correct color schema.

    """
    message = GeneralMessages.no_data_available
    state = GeneralMessages.no_data_available

    if node_status_item:
        message = node_status_item.message or message
        state = node_status_item.state or state

    formatter = None
    if should_colorize:
        formatter_structure = {
            "online": success_colored_message,
            "offline": error_colored_message,
        }
        formatter = formatter_structure.get(state)

    return formatter(message=message) if formatter else message
