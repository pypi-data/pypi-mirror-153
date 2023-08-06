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
from kelvin.sdk.lib.utils.click_utils import AppNameWithVersionType, ClickExpandedPath, KSDKCommand, KSDKGroup


@click.group(cls=KSDKGroup)
def emulation() -> bool:
    """
        Emulate and test applications locally.

        The Emulation System's simulated asset is "emulation"

        * To consume data from an application:

    \b
            - asset_names: [emulation]
              workload_names: [producer]  # equivalent to `producer:1.0.0`

        * To produce data from your application:

            - asset_names: [emulation]

    """


@emulation.command(cls=KSDKCommand)
@click.argument("app_name_with_version", nargs=1, type=AppNameWithVersionType(version_required=True), required=False)
@click.option(
    "--app-config", type=ClickExpandedPath(exists=True), required=False, help=KSDKHelpMessages.emulation_app_config
)
@click.option("--show-logs", is_flag=True, default=False, show_default=True, help=KSDKHelpMessages.show_logs)
def start(
    app_name_with_version: str,
    app_config: str,
    show_logs: bool,
) -> bool:
    """
    Start an application in the emulation system.

    """
    from kelvin.sdk.interface import emulation_start_simple

    return emulation_start_simple(
        app_name_with_version=app_name_with_version,
        app_config=app_config,
        show_logs=show_logs,
    ).success


@emulation.command(cls=KSDKCommand)
@click.argument(
    "app_name_with_version_or_container",
    type=AppNameWithVersionType(version_required=True, allow_container=True),
    nargs=1,
    required=False,
)
def stop(app_name_with_version_or_container: str) -> bool:
    """
    Stop an application running in the application system.
    \b

    Provide either the application name with its version or the container name.

    """
    from kelvin.sdk.interface import emulation_stop

    return emulation_stop(app_name_with_version_or_container=app_name_with_version_or_container).success


@emulation.command(cls=KSDKCommand)
def reset() -> bool:
    """
    Reset the emulation system.

    """
    from kelvin.sdk.interface import emulation_reset

    return emulation_reset().success


@emulation.command(cls=KSDKCommand)
@click.argument(
    "app_name_with_version_or_container",
    type=AppNameWithVersionType(version_required=True, allow_container=True),
    nargs=1,
    required=False,
)
@click.option(
    "--follow", is_flag=True, default=False, show_default=True, help=KSDKHelpMessages.emulation_logs_follow_lines
)
@click.option("--tail", type=click.INT, required=False, help=KSDKHelpMessages.emulation_logs_tail_lines)
def logs(app_name_with_version_or_container: str, follow: bool, tail: Optional[int] = None) -> bool:
    """
    Show the logs of an application running in the emulation system.

    """
    from kelvin.sdk.interface import emulation_logs

    return emulation_logs(
        app_name_with_version_or_container=app_name_with_version_or_container,
        tail=tail,
        should_print=True,
        follow=follow,
    ).success


@emulation.command(cls=KSDKCommand)
def list() -> bool:
    """
    List all applications available on the Emulation System.

    """
    from kelvin.sdk.interface import emulation_list

    return emulation_list(should_display=True).success
