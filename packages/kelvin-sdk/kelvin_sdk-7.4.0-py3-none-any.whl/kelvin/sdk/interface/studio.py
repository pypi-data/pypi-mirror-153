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

from kelvin.sdk.lib.configs.emulation_configs import StudioConfigs
from kelvin.sdk.lib.models.operation import OperationResponse


@typechecked
def studio_start(
    schema_file: Optional[str] = None,
    input_file: Optional[str] = None,
    port: int = StudioConfigs.default_port,
    open_browser: bool = False,
) -> OperationResponse:
    """
    Starts Kelvin Studio to modify the provided input.

    Parameters
    ----------
    schema_file: Optional[str]
        the schema file used to power the Kelvin Studio's interface.
    input_file: Optional[str]
        the input file to modify based on the schema file..
    port: int
        the studio server port.
    open_browser: bool
        Indicates whether Kelvin Studio should be automatically opened on the default browser.

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        an OperationResponse object encapsulating the result of the kelvin studio start.

    """
    from kelvin.sdk.lib.emulation.emulation_manager import studio_start as _studio_start

    return _studio_start(schema_file=schema_file, input_file=input_file, port=port, open_browser=open_browser)


@typechecked
def studio_stop() -> OperationResponse:
    """
    Stops a Kelvin Studio.

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        an OperationResponse object encapsulating the result of the kelvin studio stop.

    """
    from kelvin.sdk.lib.emulation.emulation_manager import studio_stop as _studio_stop

    return _studio_stop()
