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

from typing import Any

from kelvin.sdk.lib.models.operation import OperationResponse
from kelvin.sdk.server.models.parameter_models import EmulationLogsRequest, EmulationStartRequest, EmulationStopRequest
from kelvin.sdk.server.models.router import KelvinSDKServerRouter

router = KelvinSDKServerRouter(
    prefix="/emulation",
    tags=["Emulation System - [kelvin emulation]"],
    responses={404: {"description": "Not found"}},
)


@router.get("")
def emulation_list() -> Any:
    """
    Retrieve the list of all running containers in the Emulation System.
    """
    from kelvin.sdk.interface import emulation_list as _emulation_list

    return _emulation_list(should_display=False)


@router.post("/start")
def emulation_start(emulation_start_request: EmulationStartRequest) -> Any:
    """
    Start an application on the emulation system.
    """
    from kelvin.sdk.interface import emulation_start_server as _emulation_start_server

    return _emulation_start_server(
        app_config=emulation_start_request.app_config_path,
        app_name_with_version=emulation_start_request.app_name_with_version,
        tail=emulation_start_request.tail,
    )


@router.post("/stop")
def emulation_stop(emulation_stop_request: EmulationStopRequest) -> OperationResponse:
    """
    Stop a running application on the emulation system.
    """
    from kelvin.sdk.interface import emulation_stop_server as _emulation_stop_server

    return _emulation_stop_server(
        app_name_with_version=emulation_stop_request.app_name_with_version,
        container_name=emulation_stop_request.container_name,
    )


@router.post("/reset")
def emulation_reset() -> OperationResponse:
    """
    Reset the Emulation System.
    """
    from kelvin.sdk.interface import emulation_reset as _emulation_reset

    return _emulation_reset()


@router.get("/logs")
def emulation_logs(emulation_logs_request: EmulationLogsRequest) -> Any:
    """
    Display the logs of a running application.
    """
    from kelvin.sdk.interface import emulation_logs as _emulation_logs

    return _emulation_logs(
        app_name_with_version_or_container=emulation_logs_request.app_name_with_version,
        tail=emulation_logs_request.tail,
        should_print=False,
        stream=False,
        follow=False,
    )
