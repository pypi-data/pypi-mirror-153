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
import os
from tempfile import TemporaryDirectory
from typing import Optional

import uvicorn

from kelvin.sdk.lib.models.operation import OperationResponse


def server_start(
    host: str = "127.0.0.1", port: int = 8080, colored_logs: bool = False, working_dir: Optional[str] = None
) -> OperationResponse:
    """
    Jumpstart the Kelvin Server and access kelvin commands through API calls.

    Parameters
    ----------
    host: int, Default="127.0.0.1"
        the host where the server should be served.
    port: int
        the port where the server should be served.
    colored_logs: bool, Default=False
        Indicates whether all logs should be colored and 'pretty' formatted.
    working_dir: Optional[str]
        the server working directory where generated files will be store. If no dir is passed, a temporary directory
        will be used.

    Returns
    -------
    OperationResponse
        an OperationResponse encapsulating the result of the server start operation.

    """
    from kelvin.sdk.server.main import kelvin_server

    try:
        from kelvin.sdk.lib.session.session_manager import session_manager

        session_manager.setup_logger(colored_logs=colored_logs)
        if working_dir:
            os.chdir(working_dir)
            uvicorn.run(kelvin_server, port=port, host=host)
        else:
            with TemporaryDirectory() as temp_dir:
                os.chdir(temp_dir)
                uvicorn.run(kelvin_server, port=port, host=host)

        return OperationResponse(success=True)
    except Exception as exc:
        from kelvin.sdk.lib.utils.logger_utils import logger

        error_message = f"Error starting the Kelvin Server: {exc}"
        logger.error(error_message)
        return OperationResponse(success=False, log=error_message)


def server_stop() -> OperationResponse:
    """
    Stop the Kelvin Server.

    Returns
    -------
    OperationResponse
        an OperationResponse encapsulating the result of the server stop operation.

    """
    try:
        return OperationResponse(success=True)
    except Exception as exc:
        from kelvin.sdk.lib.utils.logger_utils import logger

        error_message = f"Error starting the Kelvin Server: {exc}"
        logger.error(error_message)
        return OperationResponse(success=False, log=error_message)
