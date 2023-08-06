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

import click

from kelvin.sdk.lib.configs.general_configs import KSDKHelpMessages
from kelvin.sdk.lib.utils.click_utils import KSDKCommand, KSDKGroup


@click.group(cls=KSDKGroup)
def server() -> bool:
    """
    Run Kelvin as an accessible API Server.
    """


@server.command(cls=KSDKCommand)
@click.option(
    "--host",
    "-h",
    type=click.STRING,
    required=False,
    default="127.0.0.1",
    show_default=True,
    help=KSDKHelpMessages.kelvin_server_port,
)
@click.option(
    "--port",
    "-p",
    type=click.INT,
    required=False,
    default=8080,
    show_default=True,
    help=KSDKHelpMessages.kelvin_server_port,
)
@click.option(
    "--colored-logs",
    type=click.BOOL,
    required=False,
    default=False,
    is_flag=True,
    show_default=True,
    help=KSDKHelpMessages.kelvin_server_colored_logs,
)
@click.option(
    "--working-dir",
    type=click.Path(),
    required=False,
    default=None,
    help=KSDKHelpMessages.kelvin_server_working_dir,
)
def start(host: str, port: int, colored_logs: bool, working_dir: Optional[str] = None) -> bool:
    """
    Jumpstart the Kelvin Server and access kelvin commands through API calls.

    """
    from kelvin.sdk.interface import server_start

    return server_start(host=host, port=port, colored_logs=bool(colored_logs), working_dir=working_dir).success


@server.command(cls=KSDKCommand)
def stop() -> bool:
    """
    Stop the Kelvin Server.

    """
    from kelvin.sdk.interface import server_stop

    return server_stop().success
