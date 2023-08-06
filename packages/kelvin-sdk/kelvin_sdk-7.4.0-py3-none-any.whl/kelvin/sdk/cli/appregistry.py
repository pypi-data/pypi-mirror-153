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

import click

from kelvin.sdk.lib.configs.general_configs import KSDKHelpMessages
from kelvin.sdk.lib.utils.click_utils import AppNameWithVersionType, KSDKCommand, KSDKGroup


@click.group(cls=KSDKGroup)
def appregistry() -> bool:
    """
    Manage the platform's Application Registry.

    """


@appregistry.command(cls=KSDKCommand)
def list() -> bool:
    """
    List all the available applications on the platform's Application registry.

    """
    from kelvin.sdk.interface import appregistry_list

    return appregistry_list(should_display=True).success


@appregistry.command(cls=KSDKCommand)
@click.argument("query", type=click.STRING, nargs=1)
def search(query: str) -> bool:
    """
    Search for specific apps on the platform's Application Registry.

    e.g. kelvin appregistry search "my-app"

    """
    from kelvin.sdk.interface import appregistry_search

    return appregistry_search(query=query, should_display=True).success


@appregistry.command(cls=KSDKCommand)
@click.argument("name", type=click.STRING, nargs=1)
def show(name: str) -> bool:
    """
    Show the platform details and configurations for a specific application.

    e.g. kelvin appregistry show "example-app"

    e.g. kelvin appregistry show "example-app:1.0.0"

    """
    from kelvin.sdk.interface import appregistry_show

    return appregistry_show(app_name=name, should_display=True).success


@appregistry.command(cls=KSDKCommand)
@click.option(
    "--app-dir",
    type=click.Path(exists=True),
    required=False,
    default=".",
    help=KSDKHelpMessages.app_dir,
)
@click.option(
    "--upload-datatypes",
    default=False,
    is_flag=True,
    show_default=True,
    help=KSDKHelpMessages.appregistry_upload_datatypes_upload,
)
def upload(app_dir: str, upload_datatypes: bool = False) -> bool:
    """
    Upload an application to the platform's Application Registry.

    e.g. kelvin appregistry upload --app-dir="."
    """
    from kelvin.sdk.interface import appregistry_upload

    return appregistry_upload(app_dir=app_dir, upload_datatypes=upload_datatypes).success


@appregistry.command(cls=KSDKCommand)
@click.argument("app_name_with_version", nargs=1, type=AppNameWithVersionType(version_required=False))
@click.option(
    "--local-tag",
    default=False,
    is_flag=True,
    show_default=True,
    help=KSDKHelpMessages.appregistry_download_override_local_tag,
)
def download(app_name_with_version: str, local_tag: bool) -> bool:
    """
    Download an application from the platform and make it available locally.\n

    e.g. kelvin appregistry download "example-app:1.0.0"
    """
    from kelvin.sdk.interface import appregistry_download

    return appregistry_download(app_name_with_version=app_name_with_version, override_local_tag=local_tag).success


@appregistry.command(cls=KSDKCommand)
@click.argument("app_name_with_version", nargs=1, type=AppNameWithVersionType(version_required=False))
@click.option("-y", "--yes", default=False, is_flag=True, show_default=True, help=KSDKHelpMessages.yes)
def delete(app_name_with_version: str, yes: bool) -> bool:
    """
    Delete an application from the platform's Application Registry.

    e.g. kelvin appregistry delete "example-app:1.0.0"

    """
    from kelvin.sdk.interface import appregistry_delete

    return appregistry_delete(app_name_with_version=app_name_with_version, ignore_destructive_warning=yes).success
