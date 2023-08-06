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
from click import Choice

from kelvin.sdk.lib.configs.general_configs import KSDKHelpMessages
from kelvin.sdk.lib.models.types import StatusDataSource, WorkloadFileType
from kelvin.sdk.lib.utils.click_utils import ClickExpandedPath, KSDKCommand, KSDKGroup


@click.group(cls=KSDKGroup)
def workload() -> bool:
    """
    Manage and view application workloads.

    """


@workload.command(cls=KSDKCommand)
@click.option("--node-name", type=click.STRING, required=False, help=KSDKHelpMessages.workload_list_node_name)
@click.option("--app-name", type=click.STRING, required=False, help=KSDKHelpMessages.workload_list_app_name)
@click.option(
    "--enabled",
    required=False,
    type=click.BOOL,
    default=None,
    show_default=True,
    help=KSDKHelpMessages.workload_list_enabled,
)
@click.option("--source", type=Choice(StatusDataSource.as_list()), help=KSDKHelpMessages.status_source)
def list(node_name: str, app_name: str, enabled: Optional[bool], source: str) -> bool:
    """
    List the workloads available on the platform.

    """
    from kelvin.sdk.interface import workload_list

    return workload_list(
        node_name=node_name,
        app_name=app_name,
        enabled=enabled,
        source=StatusDataSource(source),
        should_display=True,
    ).success


@workload.command(cls=KSDKCommand)
@click.argument("query", type=click.STRING, nargs=1)
@click.option("--source", type=Choice(StatusDataSource.as_list()), help=KSDKHelpMessages.status_source)
def search(query: str, source: str) -> bool:
    """
    Search for specific workloads.

    """
    from kelvin.sdk.interface import workload_search

    return workload_search(query=query, source=StatusDataSource(source), should_display=True).success


@workload.command(cls=KSDKCommand)
@click.argument("workload_name", type=click.STRING, nargs=1)
@click.option("--source", type=Choice(StatusDataSource.as_list()), help=KSDKHelpMessages.status_source)
def show(workload_name: str, source: str) -> bool:
    """
    Show the details of a specific workload.

    """
    from kelvin.sdk.interface import workload_show

    return workload_show(workload_name=workload_name, source=StatusDataSource(source), should_display=True).success


@workload.command(cls=KSDKCommand)
@click.option("--node-name", type=click.STRING, required=True, help=KSDKHelpMessages.workload_deploy_node_name)
@click.option("--workload-name", type=click.STRING, required=True, help=KSDKHelpMessages.workload_deploy_workload_name)
@click.option(
    "--workload-title",
    type=click.STRING,
    required=False,
    help=KSDKHelpMessages.workload_deploy_workload_title,
)
@click.option(
    "--app-config",
    type=ClickExpandedPath(exists=True),
    required=True,
    help=KSDKHelpMessages.workload_deploy_app_config,
)
def deploy(
    node_name: str,
    workload_name: str,
    workload_title: str,
    app_config: str,
) -> bool:
    """
    Deploy a workload with specified parameters.

    e.g. kelvin workload deploy --app-name "test-app:1.0.0" --node-name "my-node" --workload-name "my-new-workload"

    """
    from kelvin.sdk.interface import workload_deploy
    from kelvin.sdk.lib.models.workloads.ksdk_workload_deployment import WorkloadDeploymentRequest

    workload_deployment_request = WorkloadDeploymentRequest(
        node_name=node_name,
        workload_name=workload_name,
        workload_title=workload_title,
        app_config=app_config,
    )

    return workload_deploy(workload_deployment_request=workload_deployment_request).success


@workload.command(cls=KSDKCommand)
@click.argument("workload_name", type=click.STRING, nargs=1)
@click.option(
    "--workload-title",
    type=click.STRING,
    required=False,
    help=KSDKHelpMessages.workload_update_workload_title,
)
@click.option(
    "--app-config",
    type=ClickExpandedPath(exists=True),
    required=True,
    help=KSDKHelpMessages.workload_update_app_config,
)
def update(workload_name: str, workload_title: str, app_config: str) -> bool:
    """
    Update a specific workload based with new configurations.

    e.g. kelvin workload update "my-workload" --app-config app.yaml

    """
    from kelvin.sdk.interface import workload_update

    return workload_update(
        workload_name=workload_name,
        workload_title=workload_title,
        app_config=app_config,
    ).success


@workload.command(cls=KSDKCommand)
@click.argument("workload_name", type=click.STRING, nargs=1)
@click.option(
    "--tail-lines",
    type=click.INT,
    required=False,
    default=200,
    show_default=True,
    help=KSDKHelpMessages.workload_logs_tail_lines,
)
@click.option("--output-file", type=click.STRING, required=False, help=KSDKHelpMessages.workload_logs_output_file)
@click.option("--follow", default=False, is_flag=True, show_default=True, help=KSDKHelpMessages.workload_logs_follow)
def logs(workload_name: str, tail_lines: int, output_file: str, follow: bool) -> bool:
    """
    Display the logs of a specific workload.

    """
    from kelvin.sdk.interface import workload_logs

    return workload_logs(
        workload_name=workload_name, tail_lines=tail_lines, output_file=output_file, follow=follow
    ).success


@workload.command(cls=KSDKCommand)
@click.argument("workload_name", type=click.STRING, nargs=1)
@click.option("-y", "--yes", default=False, is_flag=True, show_default=True, help=KSDKHelpMessages.yes)
def undeploy(workload_name: str, yes: bool) -> bool:
    """
    Undeploy and delete a workload.

    """
    from kelvin.sdk.interface import workload_undeploy

    return workload_undeploy(workload_name=workload_name, ignore_destructive_warning=yes).success


@workload.command(cls=KSDKCommand)
@click.argument("workload_name", type=click.STRING, nargs=1)
def start(workload_name: str) -> bool:
    """
    Start a workload on a node.

    """
    from kelvin.sdk.interface import workload_start

    return workload_start(workload_name=workload_name).success


@workload.command(cls=KSDKCommand)
@click.argument("workload_name", type=click.STRING, nargs=1)
@click.option("-y", "--yes", default=False, is_flag=True, show_default=True, help=KSDKHelpMessages.yes)
def stop(workload_name: str, yes: bool) -> bool:
    """
    Stop a running workload.

    """
    from kelvin.sdk.interface import workload_stop

    return workload_stop(workload_name=workload_name, ignore_destructive_warning=yes).success


@workload.command(cls=KSDKCommand)
@click.argument("filename", type=click.STRING, nargs=1)
@click.option(
    "--file-type",
    type=Choice(WorkloadFileType.as_list()),
    required=False,
    help=KSDKHelpMessages.workload_deploy_bulk_file_type,
)
@click.option("-o", "--output-filename", type=click.STRING, required=False)
@click.option(
    "-y",
    "--ignore-failures",
    default=False,
    is_flag=True,
    show_default=True,
    help=KSDKHelpMessages.workload_deploy_bulk_ignore_failures,
)
@click.option(
    "-s",
    "--skip-successes",
    default=False,
    is_flag=True,
    show_default=True,
    help=KSDKHelpMessages.workload_deploy_bulk_skip_successes,
)
@click.option(
    "-d",
    "--dry-run",
    default=False,
    is_flag=True,
    show_default=True,
    help=KSDKHelpMessages.workload_deploy_bulk_dry_run,
)
def deploy_bulk(
    filename: str,
    file_type: Optional[str],
    output_filename: Optional[str],
    ignore_failures: bool,
    skip_successes: bool,
    dry_run: bool,
) -> bool:
    """
    Deploy workloads in bulk.
    """

    from kelvin.sdk.interface import workload_deploy_bulk

    return workload_deploy_bulk(
        filename=filename,
        file_type=file_type,
        output_filename=output_filename,
        ignore_failures=ignore_failures,
        skip_successes=skip_successes,
        dry_run=dry_run,
    ).success
