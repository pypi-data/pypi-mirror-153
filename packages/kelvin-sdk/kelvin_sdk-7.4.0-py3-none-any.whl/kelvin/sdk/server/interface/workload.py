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

from fastapi import Depends

from kelvin.sdk.interface import OperationResponse, StatusDataSource
from kelvin.sdk.lib.models.workloads.ksdk_workload_deployment import WorkloadDeploymentRequest
from kelvin.sdk.server.models.parameter_models import WorkloadListRequest, WorkloadLogsRequest, WorkloadUpdateRequest
from kelvin.sdk.server.models.router import KelvinSDKServerRouter

router = KelvinSDKServerRouter(
    prefix="/workloads",
    tags=["Workloads - [kelvin workload]"],
    responses={404: {"description": "Not found"}},
)


@router.get("")
def workload_list(workload_list_request: WorkloadListRequest = Depends(WorkloadListRequest)) -> OperationResponse:
    """
    Returns the list of workloads filtered any of the arguments.
    """

    if workload_list_request.query:
        from kelvin.sdk.interface import workload_search as _workload_search

        return _workload_search(
            query=workload_list_request.query, source=workload_list_request.source, should_display=False
        )
    else:
        from kelvin.sdk.interface import workload_list as _workload_list

        return _workload_list(
            node_name=workload_list_request.node_name,
            app_name=workload_list_request.app_name,
            enabled=workload_list_request.enabled,
            source=workload_list_request.source,
            should_display=False,
        )


@router.get("/{workload_name}")
def workload_show(workload_name: str, source: StatusDataSource) -> OperationResponse:
    """
    Show the details of the specified workload.
    """
    from kelvin.sdk.interface import workload_show as _workload_show

    return _workload_show(workload_name=workload_name, source=source, should_display=False)


@router.post("/deploy")
def workload_deploy(workload_deployment_request: WorkloadDeploymentRequest) -> OperationResponse:
    """
    Deploy a workload from the specified deploy request.
    """
    from kelvin.sdk.interface import workload_deploy as _workload_deploy

    return _workload_deploy(workload_deployment_request=workload_deployment_request)


@router.put("")
def workload_update(workload_update_request: WorkloadUpdateRequest) -> OperationResponse:
    """
    Update an existing workload with the new parameters.
    """
    from kelvin.sdk.interface import workload_update as _workload_update

    return _workload_update(
        workload_name=workload_update_request.workload_name,
        workload_title=workload_update_request.workload_title,
        app_config=workload_update_request.app_config_absolute_path,
    )


@router.get("/{workload_name}/logs")
def workload_logs(workload_logs_request: WorkloadLogsRequest = Depends(WorkloadLogsRequest)) -> OperationResponse:
    """
    Show the logs of a deployed workload.
    """
    from kelvin.sdk.interface import workload_logs as _workload_logs

    return _workload_logs(
        workload_name=workload_logs_request.workload_name,
        tail_lines=workload_logs_request.tail_lines,
        output_file=workload_logs_request.output_file_absolute_path,
        follow=workload_logs_request.follow,
    )


@router.post("/{workload_name}/undeploy")
def workload_undeploy(workload_name: str) -> OperationResponse:
    """
    Stop and delete a workload on the platform.
    """
    from kelvin.sdk.interface import workload_undeploy as _workload_undeploy

    return _workload_undeploy(workload_name=workload_name, ignore_destructive_warning=True)


@router.post("/{workload_name}/start")
def workload_start(workload_name: str) -> OperationResponse:
    """
    Start the provided workload.
    """
    from kelvin.sdk.interface import workload_start as _workload_start

    return _workload_start(workload_name=workload_name)


@router.post("/{workload_name}/stop")
def workload_stop(workload_name: str) -> OperationResponse:
    """
    Stop the provided workload.
    """
    from kelvin.sdk.interface import workload_stop as _workload_stop

    return _workload_stop(workload_name=workload_name, ignore_destructive_warning=True)
