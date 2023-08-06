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

from typeguard import typechecked

from kelvin.sdk.lib.models.operation import OperationResponse


@typechecked
def server_start(
    host: str = "127.0.0.1", port: int = 8080, colored_logs: bool = False, working_dir: Optional[str] = None
) -> OperationResponse:
    """
    Jumpstart the Kelvin Server and access kelvin commands through API calls.

    Parameters
    ----------
    host: int, Default="127.0.0.1"
        the host where the server should be served.
    port: int, Default=8080
        the port where the server should be served.
    colored_logs: bool, Default=False
        Indicates whether all logs should be colored and 'pretty' formatted.
    working_dir: Optional[str]
        the server working directory where generated files will be store. If no dir is passed, a temporary directory
        will be used.

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        an OperationResponse encapsulating the result of the server start operation.

    """
    from kelvin.sdk.server.server_manager import server_start as _server_start

    return _server_start(host=host, port=port, colored_logs=colored_logs, working_dir=working_dir)


@typechecked
def server_stop() -> OperationResponse:
    """
    Stop the Kelvin Server.

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        an OperationResponse encapsulating the result of the server stop operation.

    """
    from kelvin.sdk.server.server_manager import server_stop as _server_stop

    return _server_stop()
