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

import time
from collections import Counter
from tempfile import NamedTemporaryFile
from textwrap import indent
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple, cast

from tqdm import tqdm

from kelvin.sdk.client import Client
from kelvin.sdk.client.error import APIError
from kelvin.sdk.client.model.requests import WorkloadDeploy
from kelvin.sdk.client.model.responses import ACP as Node  # noqa: N811
from kelvin.sdk.client.model.responses import App, Workload, WorkloadLogs, WorkloadStatus, WorkloadTelemetry
from kelvin.sdk.lib.configs.general_configs import GeneralConfigs, GeneralMessages
from kelvin.sdk.lib.models.apps.ksdk_app_configuration import KelvinAppConfiguration
from kelvin.sdk.lib.models.generic import KPath
from kelvin.sdk.lib.models.ksdk_docker import DockerImageName
from kelvin.sdk.lib.models.operation import OperationResponse
from kelvin.sdk.lib.models.types import DelimiterStyle, LogColor, StatusDataSource, WorkloadFileType
from kelvin.sdk.lib.models.workloads.ksdk_workload_deployment import WorkloadDeploymentRequest, WorkloadTemplateData
from kelvin.sdk.lib.schema.schema_manager import validate_app_schema_from_app_config_file
from kelvin.sdk.lib.session.session_manager import session_manager
from kelvin.sdk.lib.utils import logger_utils
from kelvin.sdk.lib.utils.deploy_bulk_utils import load_workload_data, save_workload_data
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


def workload_list(
    query: Optional[str] = None,
    node_name: Optional[str] = None,
    app_name: Optional[str] = None,
    enabled: Optional[bool] = None,
    source: StatusDataSource = StatusDataSource.CACHE,
    should_display: bool = False,
) -> OperationResponse:
    """
    Returns the list of workloads filtered any of the arguments.

    Parameters
    ----------
    query: Optional[str]
        the query to search for.
    node_name : Optional[str]
        the name of the node to filter the workloads.
    app_name : Optional[str]
        the name of the app to filter the workloads.
    enabled : bool
        indicates whether it should filter workloads by their status.
    source : StatusDataSource
        the status data source from where to obtain data.
    should_display : bool
        specifies whether or not the display should output data.

    Returns
    -------
    OperationResponse
        An OperationResponse object encapsulating the workloads available on the platform.
    """
    try:
        workload_list_step_1 = "Retrieving workloads.."
        if query:
            workload_list_step_1 = f'Searching workloads that match "{query}"'

        logger.info(workload_list_step_1)

        if app_name:
            app_name_with_version = DockerImageName.parse(name=app_name)
            app_name = app_name_with_version.name
            app_version = app_name_with_version.version
        else:
            app_name = None
            app_version = None

        display_obj = retrieve_workload_and_workload_status_data(
            query=query,
            app_name=app_name,
            app_version=app_version,
            node_name=node_name,
            enabled=enabled,
            source=source,
            should_display=should_display,
        )

        return OperationResponse(success=True, data=display_obj.parsed_data)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error retrieving workloads: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error retrieving workloads: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def workload_show(workload_name: str, source: StatusDataSource, should_display: bool = False) -> OperationResponse:
    """
    Show the details of the specified workload.

    Parameters
    ----------
    workload_name: str
        the name of the workload.
    source: StatusDataSource
        the status data source from where to obtain data.
    should_display: bool
        specifies whether or not the display should output data.

    Returns
    -------
    OperationResponse
        an OperationResponse object encapsulating the yielded workload and its data.

    """
    try:
        workload_show_step_1 = f'Retrieving workload details for "{workload_name}"'
        base_table_title = GeneralConfigs.table_title.format(title="Workload Info")
        status_table_title = GeneralConfigs.table_title.format(title="Workload Status")
        metrics_table_title = GeneralConfigs.table_title.format(title="Workload Telemetry")

        logger.info(workload_show_step_1)

        client = session_manager.login_client_on_current_url()

        workload = client.workload.get_workload(workload_name=workload_name)
        workload_status = {
            "name": workload.name,
            "status": workload.status.dict() if workload.status else GeneralMessages.no_data_available,
        }

        workload_display = display_data_object(data=workload, should_display=False, object_title=base_table_title)
        workload_status_display = display_data_object(
            data=workload_status, should_display=False, object_title=status_table_title
        )

        workload_telemetry_display: Optional[DisplayObject]
        try:
            workload_telemetry = client.workload.get_workload_telemetry(workload_name=workload_name)
            workload_telemetry_display = retrieve_workload_telemetry_data(
                workload_telemetry_data=workload_telemetry, title=metrics_table_title
            )
        except APIError:
            workload_telemetry_display = None

        # Display Workload
        base_info = workload_display.tabulated_data
        status_info = workload_status_display.tabulated_data

        if not workload_telemetry_display:
            no_metrics = f'No workload telemetry available for "{workload_name}"'
            metrics_info = warning_colored_message(message=no_metrics)
        else:
            metrics_info = workload_telemetry_display.tabulated_data

        if should_display:
            logger.info(f"{base_info}\n{status_info}\n{metrics_info}")

        complete_workload_info = {}
        if workload_display:
            complete_workload_info["workload"] = workload_display.parsed_data
        if workload_status_display:
            complete_workload_info["workload_status"] = workload_status_display.parsed_data
        if workload_telemetry_display:
            complete_workload_info["workload_telemetry"] = workload_telemetry_display.parsed_data

        return OperationResponse(success=True, data=complete_workload_info)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error showing workload: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error showing workload: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def workload_deploy(workload_deployment_request: WorkloadDeploymentRequest) -> OperationResponse:
    """
    Deploy a workload from the specified deploy request.

    Parameters
    ----------
    workload_deployment_request: WorkloadDeploymentRequest
        the deployment object that encapsulates all the necessary parameters for deploy.

    Returns
    -------
    OperationResponse
        an OperationResponse object encapsulating the result of the workload deploy operation.

    """
    try:
        logger.info("Creating workload..")

        # 0 - Load the app configuration and validate its contents against the schema.
        app_config_file_path: KPath = KPath(workload_deployment_request.app_config)
        loaded_app_config_object = app_config_file_path.read_yaml()
        validate_app_schema_from_app_config_file(app_config=loaded_app_config_object)

        client = session_manager.login_client_on_current_url()

        if not workload_deployment_request.quiet and loaded_app_config_object:
            logger.info("Application configuration successfully loaded")

        app_configuration = KelvinAppConfiguration(**loaded_app_config_object)
        app_name_with_version = DockerImageName.parse(name=app_configuration.info.app_name_with_version)

        workload_deploy_payload: WorkloadDeploy = WorkloadDeploy(
            acp_name=workload_deployment_request.node_name,
            app_name=app_name_with_version.name,
            app_version=app_name_with_version.version,
            name=workload_deployment_request.workload_name,
            title=workload_deployment_request.workload_title or workload_deployment_request.workload_name,
            payload=loaded_app_config_object,
        )

        deploy_result = client.workload.deploy_workload(data=workload_deploy_payload)
        success_message = ""
        if not workload_deployment_request.quiet and deploy_result:
            success_message = f"""\n
                Workload "{deploy_result.name}" successfully deployed.

                To check the workload logs run the following command:
                        kelvin workload logs {deploy_result.name}

                To update this workload run the following command:
                        kelvin workload update {deploy_result.name}
            """
            logger.relevant(success_message)

        return OperationResponse(success=True, log=success_message)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error creating workload: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error creating workload: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def workload_update(workload_name: str, app_config: str, workload_title: Optional[str] = None) -> OperationResponse:
    """
    Update an existing workload with the new parameters.

    Parameters
    ----------
    workload_name: str
        the name for the workload to update.
    workload_title: Optional[str]
        the title for the  workload.
    app_config: Optional[str]
        the path to the app configuration file.

    Returns
    -------
    OperationResponse
        an OperationResponse object encapsulating the result of the workload update operation.

    """
    try:
        logger.info(f'Updating workload "{workload_name}"')

        # 0 - Load the app configuration and validate its contents against the schema.
        app_config_file_path: KPath = KPath(app_config)
        loaded_app_config_object = app_config_file_path.read_yaml()
        validate_app_schema_from_app_config_file(app_config=loaded_app_config_object)

        # 1 - fetch the specified workload
        client = session_manager.login_client_on_current_url()
        workload: Workload = client.workload.get_workload(workload_name=workload_name)

        # 2 - Confirm whether or not the retrieved workload matches the provided config
        app_configuration = KelvinAppConfiguration(**loaded_app_config_object)
        if not workload.app_name or (app_configuration.info.name != workload.app_name):
            raise ValueError("Provided configuration is not valid for the provided workload")

        app_name_with_version = DockerImageName.parse(name=app_configuration.info.app_name_with_version)

        workload_deployment_request: WorkloadDeploymentRequest = WorkloadDeploymentRequest(
            node_name=workload.acp_name,
            app_name=app_name_with_version.name_with_version,
            workload_name=workload.name,
            workload_title=workload_title or workload.title,
            app_config=app_config,
        )

        deploy_result = workload_deploy(workload_deployment_request=workload_deployment_request)

        if deploy_result:
            success_message = f'Workload "{workload_name}" successfully updated'
            logger.relevant(success_message)
            return OperationResponse(success=True, log=success_message)
        else:
            return OperationResponse(success=False, log="Error updating workload")

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error updating workload: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error updating workload: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def workload_logs(
    workload_name: str, tail_lines: str, follow: bool, output_file: Optional[str] = None
) -> OperationResponse:
    """
    Show the logs of a deployed workload.

    Parameters
    ----------
    workload_name: str
        the name of the workload.
    tail_lines: str
        the number of lines to retrieve on the logs request.
    output_file: bool
        the file to output the logs into.
    follow: Optional[str]
        a flag that indicates whether it should trail the logs, constantly requesting for more logs.

    Returns
    -------
    OperationResponse
        an OperationResponse object encapsulating the logs of the workload.

    """
    try:
        logger.info(f'Retrieving workload logs for "{workload_name}"')

        client = session_manager.login_client_on_current_url()

        _retrieve_workload_logs(
            client=client,
            workload_name=workload_name,
            since_time=None,
            tail_lines=tail_lines,
            output_file=output_file,
            follow=follow,
        )

        return OperationResponse(success=True)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error retrieving logs for workload: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error retrieving logs for workload: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def workload_undeploy(workload_name: str, ignore_destructive_warning: bool = False) -> OperationResponse:
    """
    Stop and delete a workload on the platform.

    Parameters
    ----------
    workload_name: str
        the name of the workload to be stopped and deleted.
    ignore_destructive_warning: bool
        indicates whether it should ignore the destructive warning.

    Returns
    -------
    OperationResponse
        an OperationResponse object encapsulating the result of the workload undeploy operation.

    """
    try:
        if not ignore_destructive_warning:
            workload_undeploy_confirmation: str = """
                This operation will remove the workload from the node.
                All workload local data will be lost.
            """
            ignore_destructive_warning = display_yes_or_no_question(workload_undeploy_confirmation)

        success_message = ""
        if ignore_destructive_warning:
            logger.info(f'Undeploying workload "{workload_name}"')

            client = session_manager.login_client_on_current_url()

            client.workload.undeploy_workload(workload_name=workload_name)

            success_message = f'Workload "{workload_name}" successfully undeployed'
            logger.relevant(success_message)

        return OperationResponse(success=True, log=success_message)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error undeploying workload: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error undeploying workload: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def workload_start(workload_name: str) -> OperationResponse:
    """
    Start the provided workload.

    Parameters
    ----------
    workload_name: str
        the workload to start on the platform.

    Returns
    -------
    OperationResponse
        an OperationResponse object encapsulating the result of the workload start operation.

    """
    try:
        logger.info(f'Starting workload "{workload_name}"')

        client = session_manager.login_client_on_current_url()
        client.workload.start_workload(workload_name=workload_name)

        success_message = f'Workload "{workload_name}" successfully started'
        logger.relevant(success_message)

        return OperationResponse(success=True, log=success_message)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error starting workload: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error starting workload: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def workload_stop(workload_name: str, ignore_destructive_warning: bool = False) -> OperationResponse:
    """
    Stop the provided workload.

    Parameters
    ----------
    workload_name: str
        the workload to stop on the platform.
    ignore_destructive_warning: bool
        indicates whether it should ignore the destructive warning.

    Returns
    -------
    OperationResponse
        an OperationResponse object encapsulating the result of the workload stop operation.

    """
    try:
        if not ignore_destructive_warning:
            workload_stop_confirmation: str = """
                This operation will stop the workload from running in the node.
                Persistent data will be kept intact.
            """
            ignore_destructive_warning = display_yes_or_no_question(workload_stop_confirmation)

        success_message: str = ""
        if ignore_destructive_warning:
            logger.info(f'Stopping workload "{workload_name}"')

            client = session_manager.login_client_on_current_url()
            client.workload.stop_workload(workload_name=workload_name)

            success_message = f'Workload "{workload_name}" successfully stopped'
            logger.relevant(success_message)

        return OperationResponse(success=True, log=success_message)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error stopping workload: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error stopping workload: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def workload_deploy_bulk(
    filename: str,
    file_type: Optional[str],
    output_filename: Optional[str],
    ignore_failures: bool,
    skip_successes: bool,
    dry_run: bool,
) -> OperationResponse:
    """
    Deploy workloads for nodes in bulk.

    Parameters
    ----------
    filename: str
        The filename to load the configurations from.
    file_type: Optional[str]
        The type of the workload file.
    output_filename: Optional[str]
        The output file into which the results will be written.
    ignore_failures: bool
        Ignore deployment failures and automatically continue.
    skip_successes: bool
        Skip previous successes.
    dry_run: bool
        Validate inputs only.

    Returns
    -------
    OperationResponse
        an OperationResponse object encapsulating the result of the bulk deploy procedure was successful.

    """
    try:
        logger.info("Deploying configuration in bulk..")

        file = KPath(filename).complete_path()

        if not file.is_file():
            file_not_found_error = f"File does not exist: {file}"
            logger.error(file_not_found_error)
            return OperationResponse(success=False, log=file_not_found_error)

        _file_type = WorkloadFileType.parse_file_type(file_type=file_type, file=file)

        _workload_data = load_workload_data(file=file, file_type=_file_type, field_map=None)

        results, errors = _deploy_bulk_workload(
            workload_data=cast(Sequence, _workload_data),
            ignore_failures=ignore_failures,
            skip_successes=skip_successes,
            dry_run=dry_run,
        )

        save_workload_data(
            file=file, filename=filename, output_filename=output_filename, file_type=_file_type, results=results
        )

        successful = not errors
        if successful:
            final_message = "Bulk deployment operation concluded with success"
            logger.relevant(final_message)
        else:
            final_message = "Bulk deployment operation incomplete. Please check operation logs"
            logger.warning(final_message)
        return OperationResponse(success=successful, log=final_message)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error performing the bulk deployment operation: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error performing the bulk deployment operation: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def retrieve_workload_telemetry_data(workload_telemetry_data: WorkloadTelemetry, title: str = "") -> DisplayObject:
    """
    Unpack the data provided by the WorkloadMetrics object.

    Parameters
    ----------
    workload_telemetry_data : WorkloadTelemetry
        the WorkloadTelemetry object.
    title : str
        the title to associate to the the node metrics detail info.

    Returns
    -------
    DisplayObject
        a DisplayObject containing a simplified, pretty metrics object.

    """
    final_object: dict = {}

    allocation_data = workload_telemetry_data.allocation
    cpu_utilization_data = workload_telemetry_data.cpu_utilization
    memory_usage_data = workload_telemetry_data.memory_usage
    network_data = workload_telemetry_data.network

    if allocation_data:
        final_object["Allocation"] = {
            "CPU usage": allocation_data.cpu_requests,
            "Memory usage": get_bytes_as_human_readable(input_bytes_data=allocation_data.memory_requests),
        }

    if cpu_utilization_data:
        last_cpu_utilization_entry = cpu_utilization_data[-1] if cpu_utilization_data else None
        if last_cpu_utilization_entry:
            final_object["CPU utilization"] = {
                "Timestamp (date)": get_datetime_as_human_readable(input_date=last_cpu_utilization_entry.timestamp),
                "Value": last_cpu_utilization_entry.value,
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


def retrieve_workload_and_workload_status_data(
    query: Optional[str] = None,
    app_name: Optional[str] = None,
    app_version: Optional[str] = None,
    node_name: Optional[str] = None,
    enabled: Optional[bool] = None,
    source: StatusDataSource = StatusDataSource.CACHE,
    should_display: bool = True,
) -> DisplayObject:
    """
    Centralize all calls to workloads.
    First, retrieve all workloads that match the provided criteria.
    Second, retrieve all workload status.
    Last, merge both results and yield the result.

    Parameters
    ----------
    node_name: Optional[str]
        the name of the node to filter the workloads.
    app_name: Optional[str]
        the name of the app to filter the workloads.
    app_version: Optional[str]
        the version of the app to filter the workloads.
    enabled: Optional[bool]
        indicates whether it should filter workloads by their status.
    query: Optional[str]
        the query to query specific workloads.
    source: StatusDataSource
        the status data source from where to obtain data.
    should_display: bool
        if specified, will display the results of this retrieve operation.

    Returns
    -------
    DisplayObject
        a DisplayObject containing the workload and respective status data.

    """
    client = session_manager.login_client_on_current_url()

    yielded_workloads = (
        cast(
            List,
            client.workload.list_workload(
                app_name=app_name,
                app_version=app_version,
                acp_name=node_name,
                enabled=enabled,
                search=query,
            ),  # camouflaged
        )
        or []
    )

    data_to_display = _filter_workload_status_data(workloads=yielded_workloads)

    return display_data_entries(
        data=data_to_display,
        header_names=[
            "Name",
            "Title",
            "Node Name",
            "App Name",
            "App Version",
            "Workload Status",
            "Last Seen",
        ],
        attributes=[
            "name",
            "title",
            "acp_name",
            "app_name",
            "app_version",
            "workload_status",
            "last_seen",
        ],
        table_title=GeneralConfigs.table_title.format(title="Workloads"),
        should_display=should_display,
        no_data_message="No workloads available",
    )


def _filter_workload_status_data(workloads: List[Workload]) -> List:
    """
    When provided with a list of workloads, filter the status to just include state and last_seen.

    Parameters
    ----------
    workloads: List[Workload]
        the list of workloads to combine.

    Returns
    -------
    List[]
    """
    return [
        {
            **workload,
            "workload_status": _get_parsed_workload_status(workload.status),
            "last_seen": get_datetime_as_human_readable(workload.status.last_seen)
            if workload.status
            else GeneralMessages.no_data_available,
        }
        for workload in workloads
    ]


def _retrieve_workload_logs(
    client: Client,
    workload_name: str,
    since_time: Optional[str],
    tail_lines: Optional[str],
    output_file: Optional[str],
    follow: bool = False,
) -> bool:
    """

    Parameters
    ----------
    client: Client
        the Kelvin SDK Client object used to retrieve data.
    workload_name: str
        the name of the workload.
    tail_lines: Optional[str]
        the number of lines to retrieve on the logs request.
    output_file: Optional[str]
        the file to output the logs into.
    follow: bool
        a flag that indicates whether it should trail the logs, constantly requesting for more logs.

    Returns
    -------
    bool
        a boolean indicating the end of the internal workload logs retrieval operation.

    """
    logs_for_workload: WorkloadLogs = client.workload_logs.get_workload_logs(
        workload_name=workload_name, since_time=since_time, tail_lines=tail_lines
    )

    file_path = KPath(output_file) if output_file else None

    if logs_for_workload.logs:
        for key, value in logs_for_workload.logs.items():
            log_strings = [entry for entry in value if entry]
            last_date = _extract_last_date_from_log_entries(entry=log_strings)
            entry_logs = "\n".join(log_strings)
            logger.info(entry_logs)
            # output to file
            if file_path:
                file_path.write_text(entry_logs)
            # if it should follow, return the recursive call
            if follow:
                time.sleep(10)
                return _retrieve_workload_logs(
                    client=client,
                    workload_name=workload_name,
                    since_time=last_date,
                    tail_lines=tail_lines,
                    output_file=output_file,
                    follow=follow,
                )
            # finish with success
            elif not follow and file_path:
                logger.info(f'Workload logs successfully written to "{str(file_path)}"')
    else:
        logger.warning(f'No workload logs available for "{workload_name}"')
    return True


def _extract_last_date_from_log_entries(entry: List) -> Optional[str]:
    """
    Retrieves the latest date from the provided list of logs.

    Parameters
    ----------
    entry: List
        the log entries to retrieve the data from.

    Returns
    -------
    Optional[str]
        a string containing the parsed datetime.

    """
    if entry:
        import re

        last_entry = entry[-1]
        match = re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d\+Z", last_entry)
        if match:
            return match.group()
    return None


def _get_parsed_workload_status(workload_status: Optional[WorkloadStatus] = None) -> str:
    """
    When provided with a WorkloadStatus, yield the message the message with the provided color schema and format.

    Parameters
    ----------
    workload_status_item: Optional[WorkloadStatus]
        the Workload status item containing all necessary information.

    Returns
    -------
    str
        a formatted string with the correct color schema.

    """
    message = GeneralMessages.no_data_available
    state = GeneralMessages.no_data_available

    if workload_status:
        message = workload_status.message or message
        state = workload_status.state or state

    formatter_structure = {
        "running": success_colored_message,
        "deploying": warning_colored_message,
        "stopped": warning_colored_message,
        "pending_deploy": warning_colored_message,
        "pending_start": warning_colored_message,
        "failed": error_colored_message,
        "offline": error_colored_message,
    }
    formatter = formatter_structure.get(state)

    return formatter(message=message) if formatter else message


def _deploy_bulk_workload(
    workload_data: Sequence[Dict[str, Any]],
    ignore_failures: bool = False,
    skip_successes: bool = False,
    dry_run: bool = False,
) -> Tuple[Sequence[Mapping[str, Any]], int]:
    """
    Deploy a workloads in bulk based on the input file.

    Parameters
    ----------
    workload_data: Sequence[Dict[str, Any]]
        workload deployment information.
    ignore_failures: bool
        continue if any deployment fails.
    skip_successes: bool
        skip any deployment already marked with success.
    skip_successes: bool
        validate inputs only.

    Returns
    -------
    bool
        a boolean indicating whether the bulk-workload deployment operation was successful.

    """
    data: List[WorkloadTemplateData] = []

    errors = 0
    workloads: Dict[str, int] = Counter()

    client = session_manager.login_client_on_current_url()

    nodes: Dict[str, Node] = {}
    apps: Dict[str, App] = {}

    for i, entry in enumerate(workload_data):
        entry["status"] = None
        try:
            info = WorkloadTemplateData.parse_obj(entry)
        except Exception as e:
            logger.error(f"Invalid entry: {i + 1}:\n{indent(str(e), ' ' * 2)}")
            entry["status"] = "invalid data"
            errors += 1
            continue

        data += [info]
        workloads[info.workload_name] += 1

        if info.node_name not in nodes:
            try:
                nodes[info.node_name] = client.acp.get_acp(acp_name=info.node_name)  # camouflaged
            except APIError:
                logger.error(f"Unknown node: {i + 1}: {info.node_name}")
                entry["status"] = "unknown node name"
                errors += 1
                continue

        try:
            app = apps.get(info.app_name) or client.app.get_app(app_name=info.app_name)
        except APIError:
            logger.error(f"Unknown app name: {i + 1}: {info.app_name}")
            entry["status"] = "unknown app name"
            errors += 1
            continue

        if not any(x.version == info.app_version for x in app.versions or []):
            logger.error(f"Unknown app version: {i + 1}: {info.app_version}")
            entry["status"] = "unknown app version"
            errors += 1

    if errors:
        logger.error(f"Total errors: {errors}")
        return workload_data, errors

    duplicates = {k: v for k, v in workloads.items() if v > 1}
    if duplicates:
        for info in data:
            if info.workload_name in duplicates:
                info.status = "duplicate workload"
        duplicate_names = "\n".join(f"  - {k}: {v}" for k, v in sorted(duplicates.items()))
        logger.error(f"Duplicated workload definitions:\n{duplicate_names}")
        return [x.dict() for x in data], len(duplicates)

    app_configs: List[KelvinAppConfiguration] = []

    errors = 0
    logger.info("Generating runtime configuration")
    colour = "WHITE" if logger_utils.LOG_COLOR == LogColor.COLORED else None
    for i, info in tqdm(enumerate(data), "generating runtime configuration", total=len(data), colour=colour):
        try:
            info_app_config: KPath = info.app_config
            obj = info_app_config.read_yaml(context=info.dict(), delimiter_style=DelimiterStyle.ANGULAR)
            app_configs += [KelvinAppConfiguration.parse_obj(obj)]
        except Exception as e:
            logger.error(f"Invalid runtime configuration: {i}:\n{indent(str(e), ' ' * 2)}")
            info.status = "invalid runtime"
            errors += 1
        else:
            info.status = "valid"

    if errors:
        logger.error(f"Total errors: {errors}")
        return [x.dict() for x in data], errors

    if dry_run:
        logger.info("Dry run only - no errors")
        return [x.dict() for x in data], errors

    logger.info("Deploying workloads")
    progress = tqdm(total=len(data), desc=" " * 32, colour=colour)

    errors = 0

    for i, (info, app_config) in enumerate(zip(data, app_configs)):
        if info.result == "skip" or (skip_successes and info.result == "success"):
            progress.update()
            continue

        progress.set_description(info.workload_name.ljust(32))

        with NamedTemporaryFile("wt") as temp_file:
            temp_file.write(app_config.json(exclude_none=True))
            temp_file.flush()

            app_name_with_version = DockerImageName(
                name=info.app_name, version=info.app_version, raw_name=info.app_name
            )
            workload_deployment_request = WorkloadDeploymentRequest(
                node_name=info.node_name,
                app_name=app_name_with_version.name_with_version,
                workload_name=info.workload_name,
                workload_title=info.workload_title,
                app_config=temp_file.name,
                quiet=True,
            )
            result = workload_deploy(workload_deployment_request=workload_deployment_request)

        if result.success:
            info.result = "success"
        else:
            errors += 1
            info.result = "failed"
            if ignore_failures or display_yes_or_no_question("Workload deployment failed. Continue?"):
                logger.warning(f"Skipping failed workload deployment: {i + 1}: {info.workload_name}")
            else:
                logger.warning(f"Stopping after failed workload deployment: {i + 1}: {info.workload_name}")
                break

        progress.update()

    if errors:
        logger.error(f"Total errors: {errors}")

    return [x.dict() for x in data], errors
